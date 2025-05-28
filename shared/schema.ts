import {
  pgTable,
  text,
  varchar,
  timestamp,
  jsonb,
  index,
  serial,
  integer,
  boolean,
  decimal,
} from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";
import { relations } from "drizzle-orm";

// Session storage table (required for Replit Auth)
export const sessions = pgTable(
  "sessions",
  {
    sid: varchar("sid").primaryKey(),
    sess: jsonb("sess").notNull(),
    expire: timestamp("expire").notNull(),
  },
  (table) => [index("IDX_session_expire").on(table.expire)],
);

// User storage table (required for Replit Auth)
export const users = pgTable("users", {
  id: varchar("id").primaryKey().notNull(),
  email: varchar("email").unique(),
  firstName: varchar("first_name"),
  lastName: varchar("last_name"),
  profileImageUrl: varchar("profile_image_url"),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

// Datasets table
export const datasets = pgTable("datasets", {
  id: serial("id").primaryKey(),
  userId: varchar("user_id").notNull().references(() => users.id),
  name: varchar("name").notNull(),
  type: varchar("type").notNull(), // 'proteomics', 'genomics', 'metadata'
  fileName: varchar("file_name").notNull(),
  filePath: varchar("file_path").notNull(),
  fileSize: integer("file_size").notNull(),
  status: varchar("status").notNull().default("uploaded"), // 'uploaded', 'processing', 'processed', 'error'
  uploadedAt: timestamp("uploaded_at").defaultNow(),
});

// Analyses table
export const analyses = pgTable("analyses", {
  id: serial("id").primaryKey(),
  userId: varchar("user_id").notNull().references(() => users.id),
  name: varchar("name").notNull(),
  description: text("description"),
  status: varchar("status").notNull().default("queued"), // 'queued', 'running', 'completed', 'failed'
  progress: integer("progress").default(0),
  currentStep: varchar("current_step").default("preprocessing"),
  startedAt: timestamp("started_at"),
  completedAt: timestamp("completed_at"),
  estimatedCompletion: timestamp("estimated_completion"),
  createdAt: timestamp("created_at").defaultNow(),
});

// Analysis datasets junction table
export const analysisDatasets = pgTable("analysis_datasets", {
  id: serial("id").primaryKey(),
  analysisId: integer("analysis_id").notNull().references(() => analyses.id),
  datasetId: integer("dataset_id").notNull().references(() => datasets.id),
});

// Biomarkers table
export const biomarkers = pgTable("biomarkers", {
  id: serial("id").primaryKey(),
  analysisId: integer("analysis_id").notNull().references(() => analyses.id),
  name: varchar("name").notNull(),
  type: varchar("type").notNull(), // 'mutation-based', 'expression-based', 'ptm-based'
  geneName: varchar("gene_name"),
  proteinName: varchar("protein_name"),
  chromosome: varchar("chromosome"),
  position: integer("position"),
  pValue: decimal("p_value"),
  foldChange: decimal("fold_change"),
  significance: boolean("significance").default(false),
  annotation: text("annotation"),
  // New fields for enhanced biomarker identification
  sequenceLength: integer("sequence_length"),
  uniqueAminoAcids: integer("unique_amino_acids"),
  hasMotif: boolean("has_motif").default(false),
  motifPattern: varchar("motif_pattern"),
  sequenceData: text("sequence_data"),
  biomarkerScore: decimal("biomarker_score"),
  discoveredAt: timestamp("discovered_at").defaultNow(),
});

// Results table
export const results = pgTable("results", {
  id: serial("id").primaryKey(),
  analysisId: integer("analysis_id").notNull().references(() => analyses.id),
  resultType: varchar("result_type").notNull(), // 'volcano_plot', 'heatmap', 'mutation_frequency', 'survival_curve'
  data: jsonb("data").notNull(),
  filePath: varchar("file_path"),
  createdAt: timestamp("created_at").defaultNow(),
});

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  datasets: many(datasets),
  analyses: many(analyses),
}));

export const datasetsRelations = relations(datasets, ({ one, many }) => ({
  user: one(users, {
    fields: [datasets.userId],
    references: [users.id],
  }),
  analysisDatasets: many(analysisDatasets),
}));

export const analysesRelations = relations(analyses, ({ one, many }) => ({
  user: one(users, {
    fields: [analyses.userId],
    references: [users.id],
  }),
  analysisDatasets: many(analysisDatasets),
  biomarkers: many(biomarkers),
  results: many(results),
}));

export const analysisDatasetRelations = relations(analysisDatasets, ({ one }) => ({
  analysis: one(analyses, {
    fields: [analysisDatasets.analysisId],
    references: [analyses.id],
  }),
  dataset: one(datasets, {
    fields: [analysisDatasets.datasetId],
    references: [datasets.id],
  }),
}));

export const biomarkersRelations = relations(biomarkers, ({ one }) => ({
  analysis: one(analyses, {
    fields: [biomarkers.analysisId],
    references: [analyses.id],
  }),
}));

export const resultsRelations = relations(results, ({ one }) => ({
  analysis: one(analyses, {
    fields: [results.analysisId],
    references: [analyses.id],
  }),
}));

// Insert schemas
export const insertDatasetSchema = createInsertSchema(datasets).omit({
  id: true,
  uploadedAt: true,
});

export const insertAnalysisSchema = createInsertSchema(analyses).omit({
  id: true,
  startedAt: true,
  completedAt: true,
  createdAt: true,
});

export const insertBiomarkerSchema = createInsertSchema(biomarkers).omit({
  id: true,
  discoveredAt: true,
});

export const insertResultSchema = createInsertSchema(results).omit({
  id: true,
  createdAt: true,
});

// Types
export type UpsertUser = typeof users.$inferInsert;
export type User = typeof users.$inferSelect;
export type InsertDataset = z.infer<typeof insertDatasetSchema>;
export type Dataset = typeof datasets.$inferSelect;
export type InsertAnalysis = z.infer<typeof insertAnalysisSchema>;
export type Analysis = typeof analyses.$inferSelect;
export type InsertBiomarker = z.infer<typeof insertBiomarkerSchema>;
export type Biomarker = typeof biomarkers.$inferSelect;
export type InsertResult = z.infer<typeof insertResultSchema>;
export type Result = typeof results.$inferSelect;
