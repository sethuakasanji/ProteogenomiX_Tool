import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import { FileText, Database, Dna, Info, Upload, X } from "lucide-react";

interface FileUploadProps {
  onClose?: () => void;
}

export function FileUpload({ onClose }: FileUploadProps) {
  const [selectedFiles, setSelectedFiles] = useState<{
    proteomics?: File;
    genomics?: File;
    metadata?: File;
  }>({});
  const [uploadProgress, setUploadProgress] = useState(0);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const uploadMutation = useMutation({
    mutationFn: async (data: { file: File; name: string; type: string }) => {
      const formData = new FormData();
      formData.append("file", data.file);
      formData.append("name", data.name);
      formData.append("type", data.type);

      const response = await apiRequest("POST", "/api/datasets/upload", formData);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/datasets"] });
      queryClient.invalidateQueries({ queryKey: ["/api/dashboard/stats"] });
    },
  });

  const handleFileSelect = (type: "proteomics" | "genomics" | "metadata", file: File) => {
    const allowedTypes = {
      proteomics: [".csv", ".tsv"],
      genomics: [".fasta", ".vcf"],
      metadata: [".csv", ".txt"],
    };

    const fileExt = file.name.toLowerCase().substring(file.name.lastIndexOf("."));
    if (!allowedTypes[type].includes(fileExt)) {
      toast({
        title: "Invalid file type",
        description: `Please select a file with extension: ${allowedTypes[type].join(", ")}`,
        variant: "destructive",
      });
      return;
    }

    setSelectedFiles(prev => ({ ...prev, [type]: file }));
  };

  const handleUpload = async () => {
    const files = Object.entries(selectedFiles).filter(([_, file]) => file);
    
    if (files.length === 0) {
      toast({
        title: "No files selected",
        description: "Please select at least one file to upload.",
        variant: "destructive",
      });
      return;
    }

    try {
      let completed = 0;
      for (const [type, file] of files) {
        setUploadProgress((completed / files.length) * 100);
        
        await uploadMutation.mutateAsync({
          file: file!,
          name: file!.name,
          type,
        });
        
        completed++;
        setUploadProgress((completed / files.length) * 100);
      }

      toast({
        title: "Upload successful",
        description: `${files.length} file(s) uploaded successfully.`,
      });

      setSelectedFiles({});
      setUploadProgress(0);
      onClose?.();
    } catch (error) {
      toast({
        title: "Upload failed",
        description: error instanceof Error ? error.message : "Failed to upload files",
        variant: "destructive",
      });
      setUploadProgress(0);
    }
  };

  const removeFile = (type: "proteomics" | "genomics" | "metadata") => {
    setSelectedFiles(prev => {
      const updated = { ...prev };
      delete updated[type];
      return updated;
    });
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Proteomics Upload */}
        <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-primary transition-colors cursor-pointer relative">
          <input
            type="file"
            accept=".csv,.tsv"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleFileSelect("proteomics", file);
            }}
          />
          <FileText className="h-8 w-8 text-slate-400 mx-auto mb-3" />
          <p className="text-sm font-medium text-slate-600">Proteomics Data</p>
          <p className="text-xs text-slate-500 mt-1">CSV, TSV formats</p>
          
          {selectedFiles.proteomics && (
            <div className="mt-3 p-2 bg-slate-100 rounded flex items-center justify-between">
              <span className="text-xs text-slate-700 truncate">
                {selectedFiles.proteomics.name}
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation();
                  removeFile("proteomics");
                }}
              >
                <X className="h-3 w-3" />
              </Button>
            </div>
          )}
        </div>

        {/* Genomics Upload */}
        <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-primary transition-colors cursor-pointer relative">
          <input
            type="file"
            accept=".fasta,.vcf"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleFileSelect("genomics", file);
            }}
          />
          <Dna className="h-8 w-8 text-slate-400 mx-auto mb-3" />
          <p className="text-sm font-medium text-slate-600">Genomics Data</p>
          <p className="text-xs text-slate-500 mt-1">FASTA, VCF formats</p>
          
          {selectedFiles.genomics && (
            <div className="mt-3 p-2 bg-slate-100 rounded flex items-center justify-between">
              <span className="text-xs text-slate-700 truncate">
                {selectedFiles.genomics.name}
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation();
                  removeFile("genomics");
                }}
              >
                <X className="h-3 w-3" />
              </Button>
            </div>
          )}
        </div>

        {/* Metadata Upload */}
        <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-primary transition-colors cursor-pointer relative">
          <input
            type="file"
            accept=".csv,.txt"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleFileSelect("metadata", file);
            }}
          />
          <Database className="h-8 w-8 text-slate-400 mx-auto mb-3" />
          <p className="text-sm font-medium text-slate-600">Metadata</p>
          <p className="text-xs text-slate-500 mt-1">Sample information</p>
          
          {selectedFiles.metadata && (
            <div className="mt-3 p-2 bg-slate-100 rounded flex items-center justify-between">
              <span className="text-xs text-slate-700 truncate">
                {selectedFiles.metadata.name}
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation();
                  removeFile("metadata");
                }}
              >
                <X className="h-3 w-3" />
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Upload Progress */}
      {uploadProgress > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-600">Uploading files...</span>
            <span className="text-slate-600">{Math.round(uploadProgress)}%</span>
          </div>
          <Progress value={uploadProgress} />
        </div>
      )}

      {/* Info and Actions */}
      <div className="bg-slate-50 rounded-lg p-4">
        <div className="flex items-center text-sm text-slate-600">
          <Info className="h-4 w-4 text-primary mr-2 flex-shrink-0" />
          Upload your proteomics and genomics datasets to begin automated biomarker identification
        </div>
      </div>

      <div className="flex justify-end space-x-3">
        {onClose && (
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
        )}
        <Button 
          onClick={handleUpload}
          disabled={Object.keys(selectedFiles).length === 0 || uploadMutation.isPending}
          className="bg-primary hover:bg-primary/90"
        >
          <Upload className="h-4 w-4 mr-2" />
          {uploadMutation.isPending ? "Uploading..." : "Upload Files"}
        </Button>
      </div>
    </div>
  );
}
