import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Dna, ChartLine, Database, Target, Clock, Shield } from "lucide-react";

export default function Landing() {
  const handleLogin = () => {
    window.location.href = "/api/login";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Dna className="h-8 w-8 text-primary" />
              <h1 className="text-xl font-bold text-slate-900">ProteogenomiX</h1>
            </div>
            <Button onClick={handleLogin} className="bg-primary hover:bg-primary/90">
              Sign In
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-slate-900 mb-6">
            Advanced Biomarker Identification Platform
          </h1>
          <p className="text-xl text-slate-600 mb-8 max-w-3xl mx-auto">
            Transform your proteogenomics research with our powerful platform. 
            Integrate proteomics and genomics data to discover potential biomarkers 
            with unprecedented accuracy and speed.
          </p>
          <Button 
            onClick={handleLogin}
            size="lg"
            className="bg-primary hover:bg-primary/90 text-lg px-8 py-4"
          >
            Start Your Research
          </Button>
        </div>

        {/* Features */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="border-slate-200 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                <ChartLine className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">
                Automated Analysis Pipeline
              </h3>
              <p className="text-slate-600">
                Streamlined workflow for processing proteomics and genomics datasets 
                with automated quality control and normalization.
              </p>
            </CardContent>
          </Card>

          <Card className="border-slate-200 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-success/10 rounded-lg flex items-center justify-center mb-4">
                <Target className="h-6 w-6 text-success" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">
                Mutation-Based Detection
              </h3>
              <p className="text-slate-600">
                Advanced algorithms for identifying significant sequence variations 
                and their impact on protein expression and function.
              </p>
            </CardContent>
          </Card>

          <Card className="border-slate-200 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
                <Database className="h-6 w-6 text-accent" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">
                Interactive Visualizations
              </h3>
              <p className="text-slate-600">
                Rich, interactive charts and plots for exploring your data, 
                including volcano plots, heatmaps, and survival curves.
              </p>
            </CardContent>
          </Card>

          <Card className="border-slate-200 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-warning/10 rounded-lg flex items-center justify-center mb-4">
                <Clock className="h-6 w-6 text-warning" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">
                Real-time Progress Tracking
              </h3>
              <p className="text-slate-600">
                Monitor your analyses in real-time with detailed progress indicators 
                and estimated completion times.
              </p>
            </CardContent>
          </Card>

          <Card className="border-slate-200 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-error/10 rounded-lg flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-error" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">
                Secure & Scalable
              </h3>
              <p className="text-slate-600">
                Enterprise-grade security for your sensitive research data 
                with scalable computing resources.
              </p>
            </CardContent>
          </Card>

          <Card className="border-slate-200 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-secondary/10 rounded-lg flex items-center justify-center mb-4">
                <Dna className="h-6 w-6 text-secondary" />
              </div>
              <h3 className="text-lg font-semibold text-slate-900 mb-2">
                Multi-format Support
              </h3>
              <p className="text-slate-600">
                Support for multiple file formats including CSV, FASTA, VCF, 
                and TSV for maximum compatibility.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <h2 className="text-3xl font-bold text-slate-900 mb-4">
            Ready to accelerate your research?
          </h2>
          <p className="text-lg text-slate-600 mb-8">
            Join researchers worldwide who are using ProteogenomiX to discover breakthrough biomarkers.
          </p>
          <Button 
            onClick={handleLogin}
            size="lg"
            className="bg-primary hover:bg-primary/90 text-lg px-8 py-4"
          >
            Get Started Today
          </Button>
        </div>
      </div>
    </div>
  );
}
