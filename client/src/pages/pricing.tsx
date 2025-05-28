import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import PayPalButton from "@/components/PayPalButton";
import { Check, Star, Zap, Crown, Shield, Globe } from "lucide-react";

export default function Pricing() {
  const [selectedCurrency, setSelectedCurrency] = useState("USD");
  const [showPayment, setShowPayment] = useState<string | null>(null);

  const currencies = {
    USD: { symbol: "$", name: "US Dollar" },
    EUR: { symbol: "€", name: "Euro" },
    INR: { symbol: "₹", name: "Indian Rupee" },
    GBP: { symbol: "£", name: "British Pound" }
  };

  const planPrices = {
    professional: { USD: 49, EUR: 45, INR: 4000, GBP: 39 },
    enterprise: { USD: 199, EUR: 180, INR: 16000, GBP: 159 }
  };

  const handleUpgrade = (plan: string) => {
    setShowPayment(plan);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
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

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-slate-900 mb-4">
            Choose Your Research Plan
          </h1>
          <p className="text-xl text-slate-600 max-w-3xl mx-auto">
            From individual researchers to enterprise biotech companies, 
            we have the perfect plan to accelerate your biomarker discovery.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {/* Freemium Plan */}
          <Card className="border-slate-200 relative">
            <CardHeader className="text-center pb-8">
              <CardTitle className="text-2xl font-bold text-slate-900">Researcher</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold text-slate-900">Free</span>
                <span className="text-slate-600">/month</span>
              </div>
              <p className="text-slate-600 mt-2">Perfect for academic research and learning</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">5 analyses per month</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Basic biomarker identification</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Standard visualizations</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Up to 100MB file uploads</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Community support</span>
                </div>
              </div>
              <Button className="w-full bg-slate-600 hover:bg-slate-700" disabled>
                Current Plan
              </Button>
            </CardContent>
          </Card>

          {/* Professional Plan */}
          <Card className="border-primary relative shadow-lg">
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <Badge className="bg-primary text-white px-4 py-1">
                <Star className="h-4 w-4 mr-1" />
                Most Popular
              </Badge>
            </div>
            <CardHeader className="text-center pb-8">
              <CardTitle className="text-2xl font-bold text-slate-900">Professional</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold text-primary">$49</span>
                <span className="text-slate-600">/month</span>
              </div>
              <p className="text-slate-600 mt-2">Advanced features for serious researchers</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">50 analyses per month</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Advanced biomarker naming & annotation</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Interactive visualizations</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Up to 1GB file uploads</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Priority processing</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Email support</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Export to multiple formats</span>
                </div>
              </div>
              <Button 
                className="w-full bg-primary hover:bg-primary/90"
                onClick={() => handleUpgrade('professional')}
              >
                <Zap className="h-4 w-4 mr-2" />
                Upgrade Now
              </Button>
            </CardContent>
          </Card>

          {/* Enterprise Plan */}
          <Card className="border-slate-200 relative">
            <CardHeader className="text-center pb-8">
              <CardTitle className="text-2xl font-bold text-slate-900">Enterprise</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold text-slate-900">$199</span>
                <span className="text-slate-600">/month</span>
              </div>
              <p className="text-slate-600 mt-2">For biotech companies and large research teams</p>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-3">
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Unlimited analyses</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Custom biomarker workflows</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">White-label dashboard</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Unlimited file uploads</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">Dedicated infrastructure</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">24/7 phone support</span>
                </div>
                <div className="flex items-center">
                  <Check className="h-5 w-5 text-success mr-3" />
                  <span className="text-slate-700">SLA guarantee</span>
                </div>
              </div>
              <Button 
                className="w-full bg-slate-900 hover:bg-slate-800"
                onClick={() => handleUpgrade('enterprise')}
              >
                <Crown className="h-4 w-4 mr-2" />
                Contact Sales
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Value Propositions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield className="h-8 w-8 text-primary" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900 mb-2">Research Protection</h3>
            <p className="text-slate-600">
              Your research data and discoveries are protected with enterprise-grade security and IP safeguards.
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-success/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <Zap className="h-8 w-8 text-success" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900 mb-2">Accelerated Discovery</h3>
            <p className="text-slate-600">
              Our advanced algorithms reduce biomarker identification time from weeks to hours.
            </p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-warning/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <Crown className="h-8 w-8 text-warning" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900 mb-2">Publication Ready</h3>
            <p className="text-slate-600">
              Generate publication-quality visualizations and reports directly from your analyses.
            </p>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-900 text-center mb-8">
            Frequently Asked Questions
          </h2>
          
          <div className="space-y-6">
            <Card className="border-slate-200">
              <CardContent className="p-6">
                <h3 className="font-semibold text-slate-900 mb-2">
                  How does the biomarker naming feature work?
                </h3>
                <p className="text-slate-600">
                  Our proprietary algorithm automatically generates standardized biomarker names 
                  based on gene identity, motif patterns, sequence characteristics, and chromosomal location. 
                  This ensures consistent naming across your research projects.
                </p>
              </CardContent>
            </Card>

            <Card className="border-slate-200">
              <CardContent className="p-6">
                <h3 className="font-semibold text-slate-900 mb-2">
                  Can I upgrade or downgrade my plan anytime?
                </h3>
                <p className="text-slate-600">
                  Yes! You can change your plan at any time. Upgrades take effect immediately, 
                  and downgrades will take effect at the end of your current billing cycle.
                </p>
              </CardContent>
            </Card>

            <Card className="border-slate-200">
              <CardContent className="p-6">
                <h3 className="font-semibold text-slate-900 mb-2">
                  What file formats do you support?
                </h3>
                <p className="text-slate-600">
                  We support all major bioinformatics formats including FASTA, VCF, CSV, TSV, 
                  and custom formats. Our parsing engine automatically detects and processes your data.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center mt-16">
          <h2 className="text-3xl font-bold text-slate-900 mb-4">
            Ready to accelerate your biomarker discovery?
          </h2>
          <p className="text-lg text-slate-600 mb-8">
            Join thousands of researchers who trust ProteogenomiX for their proteogenomics analysis.
          </p>
          <Button 
            size="lg"
            className="bg-primary hover:bg-primary/90 text-lg px-8 py-4"
            onClick={() => handleUpgrade('professional')}
          >
            Start Your Free Trial
          </Button>
        </div>
      </div>
    </div>
  );
}