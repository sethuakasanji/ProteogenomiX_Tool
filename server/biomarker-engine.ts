import { storage } from "./storage";
import type { InsertBiomarker } from "@shared/schema";

// Biomarker naming and identification engine based on your research
export class BiomarkerEngine {
  
  // Generate standardized biomarker names based on your research methodology
  static generateBiomarkerName(
    geneName: string, 
    proteinName: string, 
    motifPattern: string,
    sequenceLength: number,
    chromosome?: string
  ): string {
    // Follow standard biomarker naming conventions
    const genePrefix = geneName ? geneName.replace(/[^A-Za-z0-9]/g, '') : 'UNK';
    const lengthCategory = sequenceLength > 500 ? 'L' : sequenceLength > 200 ? 'M' : 'S';
    const motifCode = motifPattern === 'KR[ST]' ? 'KRS' : 'GEN';
    const chromCode = chromosome ? chromosome.replace('chr', '').toUpperCase() : 'X';
    
    // Generate unique identifier: GENE_MOTIF_LENGTH_CHROMOSOME
    return `${genePrefix}_${motifCode}_${lengthCategory}_${chromCode}`;
  }

  // Core biomarker identification algorithm from your main.py
  static async identifyBiomarkers(
    proteomicsData: string,
    genomicsData: string,
    analysisId: number
  ): Promise<InsertBiomarker[]> {
    const biomarkers: InsertBiomarker[] = [];
    
    try {
      // Parse the integrated data (simplified for web integration)
      const sequences = this.parseSequenceData(proteomicsData, genomicsData);
      
      for (const seq of sequences) {
        // Apply your research criteria
        const sequenceLength = seq.sequence.length;
        const lengthCriteria = sequenceLength > 100;
        
        // KR[ST] motif detection (your key research finding)
        const motifPattern = /KR[ST]/g;
        const hasMotif = motifPattern.test(seq.sequence);
        
        // Unique amino acid count (variability analysis)
        const uniqueAminoAcids = new Set(seq.sequence).size;
        const variabilityCriteria = uniqueAminoAcids > 15;
        
        // Exclude mitochondrial sequences
        const isNotMitochondrial = seq.chromosome !== 'MT';
        
        // Calculate biomarker score based on your criteria
        const biomarkerScore = this.calculateBiomarkerScore(
          lengthCriteria,
          hasMotif,
          variabilityCriteria,
          isNotMitochondrial
        );
        
        // Identify as biomarker if all criteria met
        const isBiomarker = lengthCriteria && hasMotif && variabilityCriteria && isNotMitochondrial;
        
        if (isBiomarker) {
          const biomarkerName = this.generateBiomarkerName(
            seq.geneName,
            seq.proteinName,
            'KR[ST]',
            sequenceLength,
            seq.chromosome
          );
          
          biomarkers.push({
            analysisId,
            name: biomarkerName,
            type: 'mutation-based',
            geneName: seq.geneName,
            proteinName: seq.proteinName,
            chromosome: seq.chromosome,
            sequenceLength,
            uniqueAminoAcids,
            hasMotif,
            motifPattern: 'KR[ST]',
            sequenceData: seq.sequence.substring(0, 1000), // Store first 1000 chars
            biomarkerScore: biomarkerScore.toString(),
            significance: true,
            annotation: `Biomarker identified using proteogenomics analysis. Sequence length: ${sequenceLength}, Unique AAs: ${uniqueAminoAcids}, Contains KR[ST] motif: ${hasMotif}`
          });
        }
      }
      
      return biomarkers;
    } catch (error) {
      console.error('Biomarker identification failed:', error);
      return [];
    }
  }

  // Calculate biomarker confidence score
  private static calculateBiomarkerScore(
    lengthCriteria: boolean,
    hasMotif: boolean,
    variabilityCriteria: boolean,
    isNotMitochondrial: boolean
  ): number {
    let score = 0;
    if (lengthCriteria) score += 25;
    if (hasMotif) score += 40; // Highest weight for your key research finding
    if (variabilityCriteria) score += 25;
    if (isNotMitochondrial) score += 10;
    return score;
  }

  // Parse sequence data (simplified for web implementation)
  private static parseSequenceData(proteomicsData: string, genomicsData: string) {
    // This would integrate with your FASTA parsing logic
    // For now, return mock structure that follows your algorithm
    return [
      {
        geneName: 'BRCA1',
        proteinName: 'BRCA1_protein',
        chromosome: '17',
        sequence: 'MKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTKRSTKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTKRSTPKRSTPKRSTPKRST'
      },
      {
        geneName: 'TP53',
        proteinName: 'TP53_protein',
        chromosome: '17',
        sequence: 'MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGPDEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAKSVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHERCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCNSSCMGGMNRRPILTIITLEDSSGNLLGRNSFEVRVCACPGRDRRTEEENLRKKGEPHHELPPGSTKRALPNNTSSSPQPKKKPLDGEYFTLQIRGRERFEMFRELNEALELKDAQAGKEPGGSRAHSSHLKSKKGQSTSRHKKLMFKTEGPDSD'
      }
    ];
  }
}