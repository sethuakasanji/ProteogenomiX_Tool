import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Shield, AlertTriangle, FileText, Users } from "lucide-react";

export default function Legal() {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="h-8 w-8 bg-primary rounded flex items-center justify-center">
                <span className="text-white font-bold text-sm">PX</span>
              </div>
              <h1 className="text-xl font-bold text-slate-900">ProteogenomiX</h1>
            </div>
            <Button variant="outline" onClick={() => window.history.back()}>
              Back to Dashboard
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Research Disclaimer */}
        <Alert className="mb-8 border-warning bg-warning/5">
          <AlertTriangle className="h-4 w-4 text-warning" />
          <AlertDescription className="text-sm">
            <strong>Research Disclaimer:</strong> The biomarkers identified by this tool are potential candidates generated through computational analysis. They are intended for research purposes only and not for clinical or diagnostic use. Users are advised to validate findings through appropriate experimental or clinical methods before application.
          </AlertDescription>
        </Alert>

        {/* Legal Navigation */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <Card className="cursor-pointer hover:shadow-md transition-shadow">
            <CardContent className="p-4 text-center">
              <FileText className="h-8 w-8 text-primary mx-auto mb-2" />
              <h3 className="font-medium">Terms of Service</h3>
            </CardContent>
          </Card>
          <Card className="cursor-pointer hover:shadow-md transition-shadow">
            <CardContent className="p-4 text-center">
              <Shield className="h-8 w-8 text-success mx-auto mb-2" />
              <h3 className="font-medium">Privacy Policy</h3>
            </CardContent>
          </Card>
          <Card className="cursor-pointer hover:shadow-md transition-shadow">
            <CardContent className="p-4 text-center">
              <Users className="h-8 w-8 text-accent mx-auto mb-2" />
              <h3 className="font-medium">Data Usage</h3>
            </CardContent>
          </Card>
          <Card className="cursor-pointer hover:shadow-md transition-shadow">
            <CardContent className="p-4 text-center">
              <AlertTriangle className="h-8 w-8 text-warning mx-auto mb-2" />
              <h3 className="font-medium">Copyright</h3>
            </CardContent>
          </Card>
        </div>

        {/* Terms of Service */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="h-5 w-5 mr-2" />
              Terms of Service
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">1. Research Use Only</h4>
              <p className="text-sm text-slate-600">
                ProteogenomiX is designed exclusively for research purposes. All biomarker identifications, 
                analyses, and results are computational predictions intended for scientific research and 
                must not be used for clinical diagnosis, treatment decisions, or medical purposes.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">2. Data Ownership and Rights</h4>
              <p className="text-sm text-slate-600">
                Users retain full ownership of their uploaded research data. ProteogenomiX processes 
                data solely for the purpose of biomarker analysis. We do not claim ownership of 
                user data or research findings.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">3. Intellectual Property</h4>
              <p className="text-sm text-slate-600">
                The biomarker identification algorithms, including KR[ST] motif detection and 
                sequence variability analysis, are proprietary methods developed by Sethupathy Selvaraj 
                through original research conducted during academic studies. All intellectual property 
                rights, including but not limited to copyrights, trade secrets, and methodological innovations, 
                belong exclusively to Sethupathy Selvaraj. Unauthorized reproduction or commercial use 
                of these methods is strictly prohibited.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">4. Validation Requirements</h4>
              <p className="text-sm text-slate-600">
                All computational predictions must be validated through appropriate experimental 
                methods before publication or further research application. ProteogenomiX results 
                are preliminary findings requiring scientific validation.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">5. Service Availability</h4>
              <p className="text-sm text-slate-600">
                We strive to maintain 99.9% uptime but cannot guarantee uninterrupted service. 
                Scheduled maintenance will be announced in advance. Users should maintain local 
                copies of important data.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Privacy Policy */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Shield className="h-5 w-5 mr-2" />
              Privacy Policy & Data Protection
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">Data Collection</h4>
              <p className="text-sm text-slate-600">
                We collect only the data necessary for biomarker analysis: uploaded files (proteomics, 
                genomics, metadata), user account information, and analysis parameters. No personal 
                research data is shared with third parties.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Data Security</h4>
              <p className="text-sm text-slate-600">
                All data is encrypted in transit and at rest using industry-standard AES-256 encryption. 
                Access is restricted to authorized systems only. Regular security audits ensure 
                data protection compliance.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Data Retention</h4>
              <p className="text-sm text-slate-600">
                User data is retained for the duration of the active subscription plus 30 days. 
                Upon account deletion, all user data is permanently removed within 7 business days. 
                Users can request data deletion at any time.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">GDPR Compliance</h4>
              <p className="text-sm text-slate-600">
                For EU researchers: You have the right to access, rectify, and delete your personal 
                data. Data processing is based on legitimate research interests. Contact us for 
                data portability requests.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Research Ethics</h4>
              <p className="text-sm text-slate-600">
                Users must ensure their research data is obtained ethically and in compliance 
                with institutional review boards and applicable regulations. ProteogenomiX is 
                not responsible for the ethical sourcing of input data.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Copyright & IP Protection */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertTriangle className="h-5 w-5 mr-2" />
              Copyright & Intellectual Property
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-2">Proprietary Algorithms - Sole Ownership</h4>
              <p className="text-sm text-slate-600">
                The biomarker identification methodology, including but not limited to KR[ST] motif 
                pattern recognition, sequence length analysis, and amino acid variability scoring, 
                constitutes original research developed and owned exclusively by Sethupathy Selvaraj. 
                This work was conducted independently during academic studies and all intellectual 
                property rights belong solely to Sethupathy Selvaraj. Protected under applicable 
                copyright laws with all rights reserved.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Research Attribution</h4>
              <p className="text-sm text-slate-600">
                Publications using ProteogenomiX results should cite the platform and acknowledge 
                the computational methods employed. A proper citation format will be provided 
                with analysis results.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">User Research Rights</h4>
              <p className="text-sm text-slate-600">
                Users retain full rights to their research findings and publications. ProteogenomiX 
                claims no ownership over user discoveries, novel biomarkers, or research outcomes 
                generated using the platform.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-2">Platform Usage Rights</h4>
              <p className="text-sm text-slate-600">
                Subscription grants usage rights for computational analysis only. Reverse engineering, 
                algorithm extraction, or unauthorized reproduction of the methodology is strictly 
                prohibited and may result in legal action.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Contact Information */}
        <Card>
          <CardHeader>
            <CardTitle>Legal Contact Information</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-slate-600 mb-4">
              For legal inquiries, privacy concerns, or intellectual property matters, 
              please contact our legal team:
            </p>
            <div className="space-y-2 text-sm">
              <p><strong>Owner:</strong> Sethupathy Selvaraj</p>
              <p><strong>Email:</strong> sethupathyselvaraj01@gmail.com</p>
              <p><strong>Contact:</strong> +91 6383824543</p>
              <p><strong>Location:</strong> India</p>
              <p><strong>Last Updated:</strong> {new Date().toLocaleDateString()}</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}