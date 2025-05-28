import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import { CheckCircle, Settings, Clock, XCircle, Pause } from "lucide-react";
import type { Analysis } from "@shared/schema";

interface AnalysisPipelineProps {
  analyses: Analysis[];
  loading: boolean;
}

export function AnalysisPipeline({ analyses, loading }: AnalysisPipelineProps) {
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const createAnalysisMutation = useMutation({
    mutationFn: async (data: { name: string; description: string; datasetIds: number[] }) => {
      const response = await apiRequest("POST", "/api/analyses", data);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/analyses"] });
      queryClient.invalidateQueries({ queryKey: ["/api/dashboard/stats"] });
      toast({
        title: "Analysis started",
        description: "Your proteogenomics analysis has been initiated.",
      });
    },
  });

  const handleStartAnalysis = () => {
    createAnalysisMutation.mutate({
      name: `Analysis ${new Date().toISOString().split('T')[0]}`,
      description: "Automated proteogenomics biomarker identification",
      datasetIds: [], // Would be populated with selected datasets
    });
  };

  const runningAnalysis = analyses.find(a => a.status === "running");
  const pipelineSteps = [
    {
      id: "preprocessing",
      name: "Data Preprocessing",
      description: "Quality control and normalization",
      icon: CheckCircle,
      status: runningAnalysis ? (
        runningAnalysis.currentStep === "preprocessing" ? "running" :
        runningAnalysis.progress > 25 ? "completed" : "pending"
      ) : "pending"
    },
    {
      id: "mutation_analysis",
      name: "Mutation Analysis",
      description: "Identifying sequence variations and protein impacts",
      icon: Settings,
      status: runningAnalysis ? (
        runningAnalysis.currentStep === "mutation_analysis" ? "running" :
        runningAnalysis.progress > 65 ? "completed" : "pending"
      ) : "pending"
    },
    {
      id: "biomarker_identification",
      name: "Biomarker Identification",
      description: "Statistical analysis and significance testing",
      icon: Clock,
      status: runningAnalysis ? (
        runningAnalysis.currentStep === "biomarker_identification" ? "running" :
        runningAnalysis.progress > 85 ? "completed" : "pending"
      ) : "pending"
    },
    {
      id: "results_generation",
      name: "Results Generation",
      description: "Visualization and report compilation",
      icon: CheckCircle,
      status: runningAnalysis ? (
        runningAnalysis.currentStep === "results_generation" ? "running" :
        runningAnalysis.progress >= 100 ? "completed" : "pending"
      ) : "pending"
    },
  ];

  if (loading) {
    return (
      <Card className="border-slate-200">
        <CardContent className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="h-6 bg-slate-200 rounded w-1/3"></div>
            <div className="space-y-3">
              {[1, 2, 3, 4].map(i => (
                <div key={i} className="h-16 bg-slate-100 rounded"></div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-slate-200">
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-slate-900">Analysis Pipeline</h3>
          {!runningAnalysis && (
            <Button 
              onClick={handleStartAnalysis}
              disabled={createAnalysisMutation.isPending}
              className="bg-primary hover:bg-primary/90"
            >
              Start Analysis
            </Button>
          )}
        </div>

        <div className="space-y-4">
          {pipelineSteps.map((step, index) => {
            const Icon = step.icon;
            const isRunning = step.status === "running";
            const isCompleted = step.status === "completed";
            const isPending = step.status === "pending";

            return (
              <div 
                key={step.id}
                className={`flex items-center p-4 rounded-lg ${
                  isRunning ? "bg-primary/5 border-l-4 border-primary" :
                  isCompleted ? "bg-slate-50" :
                  "bg-slate-50 opacity-50"
                }`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center mr-4 ${
                  isCompleted ? "bg-success" :
                  isRunning ? "bg-primary" :
                  "bg-slate-300"
                }`}>
                  {isCompleted ? (
                    <CheckCircle className="h-5 w-5 text-white" />
                  ) : isRunning ? (
                    <Settings className="h-5 w-5 text-white animate-spin" />
                  ) : (
                    <span className="text-white text-sm font-medium">{index + 1}</span>
                  )}
                </div>

                <div className="flex-1">
                  <h4 className="font-medium text-slate-900">{step.name}</h4>
                  <p className="text-sm text-slate-600">{step.description}</p>
                  
                  {isRunning && runningAnalysis && (
                    <div className="w-full bg-slate-200 rounded-full h-2 mt-2">
                      <div 
                        className="bg-primary h-2 rounded-full transition-all duration-500" 
                        style={{ width: `${runningAnalysis.progress}%` }}
                      />
                    </div>
                  )}
                </div>

                <div className="text-sm font-medium">
                  <Badge 
                    variant={isCompleted ? "default" : isRunning ? "secondary" : "outline"}
                    className={
                      isCompleted ? "bg-success/10 text-success" :
                      isRunning ? "bg-primary/10 text-primary" :
                      "text-slate-400"
                    }
                  >
                    {isCompleted ? "Completed" : isRunning ? `${runningAnalysis?.progress}%` : "Pending"}
                  </Badge>
                </div>
              </div>
            );
          })}
        </div>

        {runningAnalysis && (
          <div className="mt-6 flex justify-between items-center">
            <div className="text-sm text-slate-600">
              Estimated completion: <span className="font-medium">~15 minutes</span>
            </div>
            <Button variant="destructive" size="sm">
              <Pause className="h-4 w-4 mr-2" />
              Pause Analysis
            </Button>
          </div>
        )}

        {!runningAnalysis && analyses.length === 0 && (
          <div className="text-center py-8 text-slate-500">
            <Settings className="h-12 w-12 mx-auto mb-4 text-slate-300" />
            <h4 className="text-lg font-medium mb-2">No Active Analyses</h4>
            <p>Upload datasets and start an analysis to see the pipeline in action.</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
