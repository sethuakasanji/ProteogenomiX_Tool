import { apiRequest } from "./queryClient";

export const api = {
  // Auth
  getUser: () => fetch("/api/auth/user", { credentials: "include" }),
  
  // Dashboard
  getDashboardStats: () => fetch("/api/dashboard/stats", { credentials: "include" }),
  
  // Datasets
  uploadDataset: async (formData: FormData) => {
    return apiRequest("POST", "/api/datasets/upload", formData);
  },
  getDatasets: () => fetch("/api/datasets", { credentials: "include" }),
  
  // Analyses
  createAnalysis: async (data: any) => {
    return apiRequest("POST", "/api/analyses", data);
  },
  getAnalyses: () => fetch("/api/analyses", { credentials: "include" }),
  getAnalysis: (id: number) => fetch(`/api/analyses/${id}`, { credentials: "include" }),
  
  // Biomarkers
  getBiomarkers: (analysisId: number) => 
    fetch(`/api/analyses/${analysisId}/biomarkers`, { credentials: "include" }),
  
  // Results
  getResults: (analysisId: number) => 
    fetch(`/api/analyses/${analysisId}/results`, { credentials: "include" }),
};
