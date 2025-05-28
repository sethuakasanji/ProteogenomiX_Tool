import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { useAuth } from "@/hooks/useAuth";
import { FileUpload } from "@/components/file-upload";
import { AnalysisPipeline } from "@/components/analysis-pipeline";
import { VisualizationCharts } from "@/components/visualization-charts";
import { 
  Dna, 
  Bell, 
  ChartLine, 
  Target, 
  Database, 
  Clock,
  Search,
  Tags,
  GitBranch,
  FileDown,
  Plus,
  RefreshCw,
  Download,
  Eye,
  Pause
} from "lucide-react";

export default function Dashboard() {
  const { user } = useAuth();
  const [showUploadDialog, setShowUploadDialog] = useState(false);

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ["/api/dashboard/stats"],
  });

  const { data: analyses, isLoading: analysesLoading } = useQuery({
    queryKey: ["/api/analyses"],
  });

  const { data: datasets } = useQuery({
    queryKey: ["/api/datasets"],
  });

  const handleLogout = () => {
    window.location.href = "/api/logout";
  };

  const recentAnalyses = analyses?.slice(0, 3) || [];

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Dna className="h-8 w-8 text-primary" />
                <h1 className="text-xl font-bold text-slate-900">ProteogenomiX</h1>
              </div>
              <span className="text-sm text-slate-500 hidden sm:block">
                Advanced Biomarker Identification Platform
              </span>
            </div>
            
            <nav className="hidden md:flex items-center space-x-6">
              <span className="text-primary font-medium">Dashboard</span>
              <span className="text-slate-600 hover:text-primary transition-colors cursor-pointer">Analysis</span>
              <span className="text-slate-600 hover:text-primary transition-colors cursor-pointer">Datasets</span>
              <span className="text-slate-600 hover:text-primary transition-colors cursor-pointer">Results</span>
            </nav>

            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm">
                <Bell className="h-4 w-4" />
              </Button>
              <div className="flex items-center space-x-2">
                {user?.profileImageUrl && (
                  <img 
                    src={user.profileImageUrl} 
                    alt="Profile" 
                    className="w-8 h-8 rounded-full object-cover"
                  />
                )}
                <span className="text-sm font-medium text-slate-700">
                  {user?.firstName || user?.email}
                </span>
              </div>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Dashboard Overview */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-2">Research Dashboard</h2>
          <p className="text-slate-600">Monitor your proteogenomics analyses and discover potential biomarkers</p>
          
          {/* Research Disclaimer */}
          <div className="mt-4 p-4 bg-warning/5 border border-warning/20 rounded-lg">
            <div className="flex items-start space-x-2">
              <div className="w-5 h-5 text-warning mt-0.5">⚠️</div>
              <div>
                <p className="text-sm text-slate-700">
                  <strong>Research Disclaimer:</strong> The biomarkers identified by this tool are potential candidates generated through computational analysis. They are intended for research purposes only and not for clinical or diagnostic use. Users are advised to validate findings through appropriate experimental or clinical methods before application.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Active Analyses</p>
                  <p className="text-2xl font-bold text-slate-900">
                    {statsLoading ? "..." : stats?.activeAnalyses || 0}
                  </p>
                </div>
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                  <ChartLine className="h-6 w-6 text-primary" />
                </div>
              </div>
              <div className="mt-4 flex items-center text-sm">
                <span className="text-success font-medium">+8.2%</span>
                <span className="text-slate-500 ml-1">from last month</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Biomarkers Found</p>
                  <p className="text-2xl font-bold text-slate-900">
                    {statsLoading ? "..." : stats?.biomarkersFound || 0}
                  </p>
                </div>
                <div className="w-12 h-12 bg-success/10 rounded-lg flex items-center justify-center">
                  <Target className="h-6 w-6 text-success" />
                </div>
              </div>
              <div className="mt-4 flex items-center text-sm">
                <span className="text-success font-medium">+{stats?.biomarkersFound || 0}</span>
                <span className="text-slate-500 ml-1">this week</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Datasets Processed</p>
                  <p className="text-2xl font-bold text-slate-900">
                    {statsLoading ? "..." : stats?.datasetsProcessed || 0}
                  </p>
                </div>
                <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center">
                  <Database className="h-6 w-6 text-accent" />
                </div>
              </div>
              <div className="mt-4 flex items-center text-sm">
                <span className="text-success font-medium">100%</span>
                <span className="text-slate-500 ml-1">success rate</span>
              </div>
            </CardContent>
          </Card>

          <Card className="border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600">Computing Hours</p>
                  <p className="text-2xl font-bold text-slate-900">
                    {statsLoading ? "..." : stats?.computingHours || 0}
                  </p>
                </div>
                <div className="w-12 h-12 bg-warning/10 rounded-lg flex items-center justify-center">
                  <Clock className="h-6 w-6 text-warning" />
                </div>
              </div>
              <div className="mt-4 flex items-center text-sm">
                <span className="text-slate-500">Total usage</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="xl:col-span-2 space-y-6">
            {/* Data Upload Section */}
            <Card className="border-slate-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-slate-900">Upload Datasets</h3>
                  <Button onClick={() => setShowUploadDialog(true)} className="bg-primary hover:bg-primary/90">
                    <Plus className="h-4 w-4 mr-2" />
                    New Analysis
                  </Button>
                </div>

                <FileUpload />
              </CardContent>
            </Card>

            {/* Analysis Pipeline */}
            <AnalysisPipeline analyses={recentAnalyses} loading={analysesLoading} />

            {/* Recent Results */}
            <Card className="border-slate-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-semibold text-slate-900">Recent Results</h3>
                  <Button variant="ghost" className="text-primary hover:text-primary/80">
                    View All
                  </Button>
                </div>

                <div className="space-y-4">
                  {recentAnalyses.length === 0 ? (
                    <div className="text-center py-8 text-slate-500">
                      No analyses yet. Upload datasets to get started.
                    </div>
                  ) : (
                    recentAnalyses.map((analysis) => (
                      <div key={analysis.id} className="flex items-center justify-between p-4 border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors">
                        <div className="flex items-center space-x-4">
                          <div className="w-10 h-10 bg-success/10 rounded-lg flex items-center justify-center">
                            <ChartLine className="h-5 w-5 text-success" />
                          </div>
                          <div>
                            <h4 className="font-medium text-slate-900">{analysis.name}</h4>
                            <p className="text-sm text-slate-600">
                              {analysis.description} • {new Date(analysis.createdAt).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-3">
                          <Badge 
                            variant={analysis.status === "completed" ? "default" : analysis.status === "running" ? "secondary" : "outline"}
                            className={analysis.status === "completed" ? "bg-success/10 text-success" : analysis.status === "running" ? "bg-primary/10 text-primary" : ""}
                          >
                            {analysis.status === "completed" ? "Complete" : analysis.status === "running" ? "Running" : "Queued"}
                          </Badge>
                          <Button variant="ghost" size="sm">
                            {analysis.status === "completed" ? <Download className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                          </Button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Quick Tools */}
            <Card className="border-slate-200">
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">Quick Tools</h3>
                
                <div className="space-y-3">
                  <Button variant="outline" className="w-full justify-start">
                    <Search className="h-4 w-4 mr-3" />
                    <div className="text-left">
                      <p className="font-medium">Biomarker Search</p>
                      <p className="text-xs text-slate-600">Find existing biomarkers</p>
                    </div>
                  </Button>

                  <Button variant="outline" className="w-full justify-start">
                    <Tags className="h-4 w-4 mr-3" />
                    <div className="text-left">
                      <p className="font-medium">Annotation Tool</p>
                      <p className="text-xs text-slate-600">Add biomarker metadata</p>
                    </div>
                  </Button>

                  <Button variant="outline" className="w-full justify-start">
                    <GitBranch className="h-4 w-4 mr-3" />
                    <div className="text-left">
                      <p className="font-medium">Pathway Analysis</p>
                      <p className="text-xs text-slate-600">Explore biological pathways</p>
                    </div>
                  </Button>

                  <Button variant="outline" className="w-full justify-start">
                    <FileDown className="h-4 w-4 mr-3" />
                    <div className="text-left">
                      <p className="font-medium">Export Results</p>
                      <p className="text-xs text-slate-600">Download analysis reports</p>
                    </div>
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Biomarker Insights */}
            <VisualizationCharts />

            {/* System Status */}
            <Card className="border-slate-200">
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold text-slate-900 mb-4">System Status</h3>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="w-2 h-2 bg-success rounded-full mr-3"></div>
                      <span className="text-sm text-slate-600">Analysis Engine</span>
                    </div>
                    <span className="text-sm font-medium text-success">Online</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="w-2 h-2 bg-success rounded-full mr-3"></div>
                      <span className="text-sm text-slate-600">Database</span>
                    </div>
                    <span className="text-sm font-medium text-success">Connected</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="w-2 h-2 bg-warning rounded-full mr-3"></div>
                      <span className="text-sm text-slate-600">Queue</span>
                    </div>
                    <span className="text-sm font-medium text-warning">{stats?.activeAnalyses || 0} jobs</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className="w-2 h-2 bg-success rounded-full mr-3"></div>
                      <span className="text-sm text-slate-600">Storage</span>
                    </div>
                    <span className="text-sm font-medium text-slate-600">2.4TB free</span>
                  </div>
                </div>

                <Separator className="my-4" />

                <div>
                  <div className="text-xs text-slate-500 mb-2">CPU Usage</div>
                  <Progress value={32} className="h-2" />
                  <div className="text-xs text-slate-500 mt-1">32% of 128 cores</div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Detailed Visualization Section */}
        <div className="mt-8">
          <Card className="border-slate-200">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-slate-900">Interactive Analysis Results</h3>
                <div className="flex items-center space-x-3">
                  <select className="px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white">
                    <option>Select Analysis</option>
                    {recentAnalyses.map(analysis => (
                      <option key={analysis.id} value={analysis.id}>
                        {analysis.name}
                      </option>
                    ))}
                  </select>
                  <Button variant="outline" size="sm">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh
                  </Button>
                </div>
              </div>

              {recentAnalyses.length === 0 ? (
                <div className="text-center py-12 text-slate-500">
                  <ChartLine className="h-12 w-12 mx-auto mb-4 text-slate-300" />
                  <h4 className="text-lg font-medium mb-2">No Analysis Results</h4>
                  <p>Complete an analysis to view interactive visualizations and charts.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                  <div className="border border-slate-200 rounded-lg p-4">
                    <h4 className="font-medium text-slate-900 mb-3">Volcano Plot - Protein Expression</h4>
                    <div className="h-80 bg-slate-50 rounded flex items-center justify-center text-slate-500">
                      Interactive Plotly volcano plot will be rendered here
                    </div>
                  </div>

                  <div className="border border-slate-200 rounded-lg p-4">
                    <h4 className="font-medium text-slate-900 mb-3">Biomarker Expression Heatmap</h4>
                    <div className="h-80 bg-slate-50 rounded flex items-center justify-center text-slate-500">
                      Interactive Plotly heatmap will be rendered here
                    </div>
                  </div>

                  <div className="border border-slate-200 rounded-lg p-4">
                    <h4 className="font-medium text-slate-900 mb-3">Mutation Frequency Analysis</h4>
                    <div className="h-80 bg-slate-50 rounded flex items-center justify-center text-slate-500">
                      Interactive Plotly bar chart will be rendered here
                    </div>
                  </div>

                  <div className="border border-slate-200 rounded-lg p-4">
                    <h4 className="font-medium text-slate-900 mb-3">Biomarker-based Survival Curves</h4>
                    <div className="h-80 bg-slate-50 rounded flex items-center justify-center text-slate-500">
                      Interactive Plotly line chart will be rendered here
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {showUploadDialog && (
        <FileUpload onClose={() => setShowUploadDialog(false)} />
      )}
    </div>
  );
}
