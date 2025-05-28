import {
  users,
  datasets,
  analyses,
  analysisDatasets,
  biomarkers,
  results,
  type User,
  type UpsertUser,
  type Dataset,
  type InsertDataset,
  type Analysis,
  type InsertAnalysis,
  type Biomarker,
  type InsertBiomarker,
  type Result,
  type InsertResult,
} from "@shared/schema";
import { db } from "./db";
import { eq, desc, and } from "drizzle-orm";

export interface IStorage {
  // User operations (required for Replit Auth)
  getUser(id: string): Promise<User | undefined>;
  upsertUser(user: UpsertUser): Promise<User>;
  
  // Dataset operations
  createDataset(dataset: InsertDataset): Promise<Dataset>;
  getDatasetsByUserId(userId: string): Promise<Dataset[]>;
  getDataset(id: number): Promise<Dataset | undefined>;
  updateDatasetStatus(id: number, status: string): Promise<void>;
  
  // Analysis operations
  createAnalysis(analysis: InsertAnalysis): Promise<Analysis>;
  getAnalysesByUserId(userId: string): Promise<Analysis[]>;
  getAnalysis(id: number): Promise<Analysis | undefined>;
  updateAnalysisProgress(id: number, progress: number, currentStep?: string): Promise<void>;
  updateAnalysisStatus(id: number, status: string): Promise<void>;
  
  // Analysis-Dataset associations
  linkAnalysisDataset(analysisId: number, datasetId: number): Promise<void>;
  
  // Biomarker operations
  createBiomarker(biomarker: InsertBiomarker): Promise<Biomarker>;
  getBiomarkersByAnalysisId(analysisId: number): Promise<Biomarker[]>;
  
  // Result operations
  createResult(result: InsertResult): Promise<Result>;
  getResultsByAnalysisId(analysisId: number): Promise<Result[]>;
  
  // Dashboard statistics
  getDashboardStats(userId: string): Promise<{
    activeAnalyses: number;
    biomarkersFound: number;
    datasetsProcessed: number;
    computingHours: number;
  }>;
}

export class DatabaseStorage implements IStorage {
  // User operations (required for Replit Auth)
  async getUser(id: string): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user;
  }

  async upsertUser(userData: UpsertUser): Promise<User> {
    const [user] = await db
      .insert(users)
      .values(userData)
      .onConflictDoUpdate({
        target: users.id,
        set: {
          ...userData,
          updatedAt: new Date(),
        },
      })
      .returning();
    return user;
  }

  // Dataset operations
  async createDataset(dataset: InsertDataset): Promise<Dataset> {
    const [newDataset] = await db.insert(datasets).values(dataset).returning();
    return newDataset;
  }

  async getDatasetsByUserId(userId: string): Promise<Dataset[]> {
    return await db
      .select()
      .from(datasets)
      .where(eq(datasets.userId, userId))
      .orderBy(desc(datasets.uploadedAt));
  }

  async getDataset(id: number): Promise<Dataset | undefined> {
    const [dataset] = await db.select().from(datasets).where(eq(datasets.id, id));
    return dataset;
  }

  async updateDatasetStatus(id: number, status: string): Promise<void> {
    await db.update(datasets).set({ status }).where(eq(datasets.id, id));
  }

  // Analysis operations
  async createAnalysis(analysis: InsertAnalysis): Promise<Analysis> {
    const [newAnalysis] = await db.insert(analyses).values(analysis).returning();
    return newAnalysis;
  }

  async getAnalysesByUserId(userId: string): Promise<Analysis[]> {
    return await db
      .select()
      .from(analyses)
      .where(eq(analyses.userId, userId))
      .orderBy(desc(analyses.createdAt));
  }

  async getAnalysis(id: number): Promise<Analysis | undefined> {
    const [analysis] = await db.select().from(analyses).where(eq(analyses.id, id));
    return analysis;
  }

  async updateAnalysisProgress(id: number, progress: number, currentStep?: string): Promise<void> {
    const updateData: any = { progress };
    if (currentStep) updateData.currentStep = currentStep;
    
    await db.update(analyses).set(updateData).where(eq(analyses.id, id));
  }

  async updateAnalysisStatus(id: number, status: string): Promise<void> {
    const updateData: any = { status };
    if (status === "running") updateData.startedAt = new Date();
    if (status === "completed" || status === "failed") updateData.completedAt = new Date();
    
    await db.update(analyses).set(updateData).where(eq(analyses.id, id));
  }

  // Analysis-Dataset associations
  async linkAnalysisDataset(analysisId: number, datasetId: number): Promise<void> {
    await db.insert(analysisDatasets).values({ analysisId, datasetId });
  }

  // Biomarker operations
  async createBiomarker(biomarker: InsertBiomarker): Promise<Biomarker> {
    const [newBiomarker] = await db.insert(biomarkers).values(biomarker).returning();
    return newBiomarker;
  }

  async getBiomarkersByAnalysisId(analysisId: number): Promise<Biomarker[]> {
    return await db
      .select()
      .from(biomarkers)
      .where(eq(biomarkers.analysisId, analysisId))
      .orderBy(desc(biomarkers.discoveredAt));
  }

  // Result operations
  async createResult(result: InsertResult): Promise<Result> {
    const [newResult] = await db.insert(results).values(result).returning();
    return newResult;
  }

  async getResultsByAnalysisId(analysisId: number): Promise<Result[]> {
    return await db
      .select()
      .from(results)
      .where(eq(results.analysisId, analysisId))
      .orderBy(desc(results.createdAt));
  }

  // Dashboard statistics
  async getDashboardStats(userId: string): Promise<{
    activeAnalyses: number;
    biomarkersFound: number;
    datasetsProcessed: number;
    computingHours: number;
  }> {
    const userAnalyses = await db
      .select()
      .from(analyses)
      .where(eq(analyses.userId, userId));

    const activeAnalyses = userAnalyses.filter(a => 
      a.status === "running" || a.status === "queued"
    ).length;

    const userBiomarkers = await db
      .select()
      .from(biomarkers)
      .innerJoin(analyses, eq(biomarkers.analysisId, analyses.id))
      .where(eq(analyses.userId, userId));

    const userDatasets = await db
      .select()
      .from(datasets)
      .where(and(eq(datasets.userId, userId), eq(datasets.status, "processed")));

    // Mock computing hours calculation
    const computingHours = userAnalyses.reduce((total, analysis) => {
      if (analysis.completedAt && analysis.startedAt) {
        const hours = (analysis.completedAt.getTime() - analysis.startedAt.getTime()) / (1000 * 60 * 60);
        return total + hours;
      }
      return total;
    }, 0);

    return {
      activeAnalyses,
      biomarkersFound: userBiomarkers.length,
      datasetsProcessed: userDatasets.length,
      computingHours: Math.round(computingHours),
    };
  }
}

export const storage = new DatabaseStorage();
