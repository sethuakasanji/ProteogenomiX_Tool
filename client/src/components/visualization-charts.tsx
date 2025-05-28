import { useEffect, useRef } from "react";
import { Card, CardContent } from "@/components/ui/card";

export function VisualizationCharts() {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Check if Plotly is available
    if (typeof window !== 'undefined' && (window as any).Plotly && chartRef.current) {
      const data = [{
        values: [156, 124, 67],
        labels: ['Mutation-based', 'Expression-based', 'PTM-based'],
        type: 'pie',
        marker: {
          colors: ['#2563EB', '#10B981', '#F59E0B']
        },
        textinfo: 'label+percent',
        textposition: 'inside'
      }];

      const layout = {
        margin: { t: 20, b: 20, l: 20, r: 20 },
        font: { family: 'Inter, sans-serif', size: 12 },
        showlegend: false,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent'
      };

      const config = {
        responsive: true,
        displayModeBar: false
      };

      (window as any).Plotly.newPlot(chartRef.current, data, layout, config);
    }
  }, []);

  return (
    <Card className="border-slate-200">
      <CardContent className="p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Biomarker Distribution</h3>
        
        {/* Chart Container */}
        <div ref={chartRef} className="h-64 mb-4" />
        
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-primary rounded-full mr-2"></div>
              <span className="text-slate-600">Mutation-based</span>
            </div>
            <span className="font-medium text-slate-900">156</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-success rounded-full mr-2"></div>
              <span className="text-slate-600">Expression-based</span>
            </div>
            <span className="font-medium text-slate-900">124</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-warning rounded-full mr-2"></div>
              <span className="text-slate-600">PTM-based</span>
            </div>
            <span className="font-medium text-slate-900">67</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
