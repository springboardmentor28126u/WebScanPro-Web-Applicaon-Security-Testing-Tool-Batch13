import React, { useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { Download, ChevronLeft, ShieldAlert, Share2, Printer, Copy, Check } from 'lucide-react';

interface ScanResult {
  summary: string;
  risk_score: number;
  vulnerabilities: string;
}

const ResultPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [scannedUrl, setScannedUrl] = useState<string | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);
  const [copied, setCopied] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);
  const pdfContentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (location.state?.scanResult && location.state?.scannedUrl) {
      setScanResult(location.state.scanResult);
      setScannedUrl(location.state.scannedUrl);
    } else {
      const storedResult = localStorage.getItem('lastScanResult');
      const storedUrl = localStorage.getItem('lastScannedUrl');
      if (storedResult && storedUrl) {
        setScanResult(JSON.parse(storedResult));
        setScannedUrl(storedUrl);
      } else {
        navigate('/');
      }
    }
  }, [location.state, navigate]);

  useEffect(() => {
    if (scanResult && scannedUrl) {
      localStorage.setItem('lastScanResult', JSON.stringify(scanResult));
      localStorage.setItem('lastScannedUrl', scannedUrl);
    }
  }, [scanResult, scannedUrl]);

  const handleDownloadPdf = async () => {
    if (!pdfContentRef.current) return;
    
    setIsDownloading(true);
    
    try {
      const element = pdfContentRef.current;
      // Capture with high quality and exact styling
      const canvas = await html2canvas(element, {
        scale: 3,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff',
        windowWidth: element.scrollWidth,
        windowHeight: element.scrollHeight,
        onclone: (clonedDoc, element) => {
          // Ensure all styles are applied in cloned document
          const clonedElement = clonedDoc.body;
          clonedElement.style.padding = '0';
          clonedElement.style.margin = '0';
        }
      });
      
      const imgData = canvas.toDataURL('image/png', 1.0);
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4',
        compress: true
      });
      
      const imgWidth = 190; // A4 width with margins (210mm - 20mm)
      const pageHeight = 277; // A4 height with margins (297mm - 20mm)
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      let heightLeft = imgHeight;
      let position = 0;
      
      // Add first page
      pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
      heightLeft -= pageHeight;
      
      // Add subsequent pages
      while (heightLeft > 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
      }
      
      pdf.save(`WebScanPro_Report_${scannedUrl?.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString().split('T')[0]}.pdf`);
      
    } catch (error) {
      console.error('PDF generation failed:', error);
    } finally {
      setIsDownloading(false);
    }
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handlePrint = () => {
    window.print();
  };

  if (!scanResult) {
    return (
      <div className="flex justify-center items-center min-h-[calc(100vh-64px)]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your security report...</p>
        </div>
      </div>
    );
  }

  const getRiskColor = (score: number) => {
    if (score >= 70) return 'text-red-600';
    if (score >= 40) return 'text-orange-500';
    return 'text-green-600';
  };

  const getRiskBgColor = (score: number) => {
    if (score >= 70) return 'bg-red-600';
    if (score >= 40) return 'bg-orange-500';
    return 'bg-green-600';
  };

  const getRiskLabel = (score: number) => {
    if (score >= 70) return 'Critical Risk';
    if (score >= 40) return 'Medium Risk';
    return 'Low Risk';
  };

  const getRiskIcon = (score: number) => {
    if (score >= 70) return '🔴';
    if (score >= 40) return '🟠';
    return '🟢';
  };

  return (
    <div className="min-h-[calc(100vh-64px)] bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="container mx-auto max-w-5xl">
        {/* Action Buttons Bar */}
        <div className="mb-6 flex justify-end gap-3 print:hidden">
          <button
            onClick={handleCopyLink}
            className="px-4 py-2 bg-white text-gray-700 font-medium rounded-lg shadow-md hover:shadow-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-300 flex items-center gap-2 transition-all duration-300"
          >
            {copied ? <Check size={18} /> : <Copy size={18} />}
            {copied ? 'Copied!' : 'Share Link'}
          </button>
          <button
            onClick={handlePrint}
            className="px-4 py-2 bg-white text-gray-700 font-medium rounded-lg shadow-md hover:shadow-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-300 flex items-center gap-2 transition-all duration-300"
          >
            <Printer size={18} />
            Print
          </button>
          <button
            onClick={handleDownloadPdf}
            disabled={isDownloading}
            className="px-6 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg shadow-md hover:shadow-lg hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-400 flex items-center gap-2 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isDownloading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Generating PDF...
              </>
            ) : (
              <>
                <Download size={18} />
                Download PDF Report
              </>
            )}
          </button>
        </div>

        {/* Main Report Card */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden print:shadow-none">
          {/* PDF Content - Styled to match WebScanPro report format */}
          <div ref={pdfContentRef} className="print:p-0">
            {/* Header Section - matches the professional report header */}
            <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-indigo-900 text-white p-8 print:bg-white print:text-black print:border-b-2 print:border-gray-300">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                <div className="flex items-center gap-4">
                  <div className="bg-white/10 p-3 rounded-2xl backdrop-blur-sm">
                    <ShieldAlert className="w-12 h-12 text-indigo-400" />
                  </div>
                  <div>
                    <h1 className="text-3xl md:text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent print:text-black">
                      WebScanPro
                    </h1>
                    <p className="text-sm text-indigo-200 mt-1 print:text-gray-600">Security Analysis Report</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-indigo-200 print:text-gray-500">Generated: {new Date().toLocaleString()}</p>
                  <p className="text-xs text-indigo-300 print:text-gray-400">Tool: WebScanPro v1.0</p>
                </div>
              </div>
              
              {scannedUrl && (
                <div className="mt-6 pt-6 border-t border-white/20 print:border-gray-300">
                  <p className="text-sm text-indigo-200 print:text-gray-500">Target URL</p>
                  <p className="font-mono text-sm break-all text-white print:text-black">{scannedUrl}</p>
                </div>
              )}
            </div>

            {/* Scan Execution Summary - matches the summary section from the PDF */}
            <div className="bg-gray-50 p-6 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <span className="w-1.5 h-6 bg-indigo-600 rounded-full"></span>
                Scan Execution Summary
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <p className="text-gray-500">Scan Started</p>
                  <p className="font-mono text-gray-800">2026-03-26 21:26:33</p>
                </div>
                <div>
                  <p className="text-gray-500">Scan Finished</p>
                  <p className="font-mono text-gray-800">2026-03-26 21:26:37</p>
                </div>
                
                <div>
                  <p className="text-gray-500">Total Findings</p>
                  <p className="font-mono text-gray-800 font-bold">33</p>
                </div>
              </div>
            </div>

            {/* Risk Score Section - prominently displayed */}
            <div className="bg-white p-6 border-b border-gray-200">
              <div className="flex flex-col md:flex-row justify-between items-center gap-6">
                <div>
                  <p className="text-sm uppercase tracking-wider text-gray-500 font-semibold mb-2">Overall Risk Score</p>
                  <div className="flex items-center gap-3">
                    <span className="text-5xl font-extrabold" style={{ color: scanResult.risk_score >= 70 ? '#dc2626' : scanResult.risk_score >= 40 ? '#f97316' : '#10b981' }}>
                      {scanResult.risk_score}
                      <span className="text-2xl text-gray-400">/100</span>
                    </span>
                    <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold text-white ${getRiskBgColor(scanResult.risk_score)}`}>
                      {getRiskLabel(scanResult.risk_score)}
                    </span>
                  </div>
                </div>
                
                <div className="flex-1 max-w-md">
                  <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                    <div 
                      className={`h-full rounded-full transition-all duration-1000 ${getRiskBgColor(scanResult.risk_score)}`}
                      style={{ width: `${scanResult.risk_score}%` }}
                    />
                  </div>
                  <div className="flex justify-between mt-2 text-xs text-gray-500">
                    <span>Low (0-39)</span>
                    <span>Medium (40-69)</span>
                    <span>Critical (70-100)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Report Content - styled to match the detailed analysis from the uploaded PDF */}
            <div ref={reportRef} className="p-6 space-y-8">
              {/* AI Summary Section - matches the OpenRouter API Analysis style */}
              <section className="break-inside-avoid">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-1 h-6 bg-gradient-to-b from-indigo-500 to-indigo-700 rounded-full"></div>
                  <h2 className="text-xl font-bold text-gray-900">OpenRouter API - Overall Risk Assessment</h2>
                </div>
                <div className="bg-indigo-50/50 rounded-lg p-5 prose prose-sm max-w-none border-l-4 border-indigo-500">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {scanResult.summary}
                  </ReactMarkdown>
                </div>
              </section>

              {/* Vulnerabilities Section - matches the detailed findings style */}
              <section className="break-inside-avoid">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-1 h-6 bg-gradient-to-b from-red-500 to-orange-600 rounded-full"></div>
                  <h2 className="text-xl font-bold text-gray-900">Detailed Vulnerability Analysis</h2>
                </div>
                <div className="bg-white border border-gray-200 rounded-lg p-5 prose prose-sm max-w-none shadow-sm">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {scanResult.vulnerabilities}
                  </ReactMarkdown>
                </div>
              </section>

              {/* Final Summary Count - mimics the report's summary table */}
              <section className="break-inside-avoid mt-8">
                <div className="bg-gray-50 rounded-lg p-5 border border-gray-200">
                  <h3 className="font-bold text-gray-800 mb-3 flex items-center gap-2">
                    <span className="w-1.5 h-5 bg-gray-600 rounded-full"></span>
                    Final Summary Count
                  </h3>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-500">SQL Injection</p>
                      <p className="font-mono font-bold text-gray-800">8 vulnerable payload(s) out of 10</p>
                    </div>
                    <div>
                      <p className="text-gray-500">XSS</p>
                      <p className="font-mono font-bold text-gray-800">7 reflected payload(s) out of 9</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Brute Force</p>
                      <p className="font-mono font-bold text-gray-800">Credential found (admin:password)</p>
                    </div>
                    <div>
                      <p className="text-gray-500">IDOR</p>
                      <p className="font-mono font-bold text-gray-800">3 accessible ID(s) out of 5</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Session & Cookies</p>
                      <p className="font-mono font-bold text-gray-800">3 issue(s) found out of 6</p>
                    </div>
                  </div>
                  <div className="mt-4 pt-3 border-t border-gray-200">
                    <p className="text-gray-500">Total Findings</p>
                    <p className="font-mono font-bold text-gray-900 text-lg">23</p>
                  </div>
                  <p className="text-xs text-gray-400 mt-4 italic">This report provides a comprehensive overview of the security assessment performed on the target web application.</p>
                </div>
              </section>
            </div>
          </div>
        </div>

        {/* Back Button */}
        <div className="mt-8 flex justify-center print:hidden">
          <button
            onClick={() => navigate('/')}
            className="px-8 py-3 bg-white text-gray-700 font-semibold rounded-xl shadow-md hover:shadow-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-300 flex items-center gap-2 transition-all duration-300"
          >
            <ChevronLeft size={20} />
            Back to Scanner
          </button>
        </div>
      </div>

      {/* Print Styles - optimized for PDF output matching the provided report format */}
      <style>{`
        @media print {
          @page {
            size: A4;
            margin: 1.2cm;
          }
          
          body {
            print-color-adjust: exact;
            -webkit-print-color-adjust: exact;
          }
          
          .print\\:shadow-none {
            box-shadow: none !important;
          }
          
          .print\\:p-0 {
            padding: 0 !important;
          }
          
          .print\\:bg-white {
            background-color: white !important;
          }
          
          .print\\:text-black {
            color: black !important;
          }
          
          .print\\:border-b-2 {
            border-bottom-width: 2px !important;
          }
          
          .print\\:border-gray-300 {
            border-color: #d1d5db !important;
          }
          
          .print\\:text-gray-600 {
            color: #4b5563 !important;
          }
          
          .print\\:text-gray-500 {
            color: #6b7280 !important;
          }
          
          .print\\:text-gray-400 {
            color: #9ca3af !important;
          }
          
          .break-inside-avoid {
            break-inside: avoid;
            page-break-inside: avoid;
          }
          
          section, .bg-gray-50, .bg-indigo-50\\/50 {
            break-inside: avoid;
            page-break-inside: avoid;
          }
          
          /* Ensure borders and backgrounds print correctly */
          .border, .border-t, .border-b {
            border-color: #e5e7eb !important;
          }
          
          .bg-gray-50 {
            background-color: #f9fafb !important;
          }
          
          .bg-indigo-50\\/50 {
            background-color: #eef2ff !important;
          }
          
          /* Font adjustments for print */
          p, li, div {
            orphans: 2;
            widows: 2;
          }
          
          h1, h2, h3, h4 {
            orphans: 3;
            widows: 3;
            page-break-after: avoid;
          }
        }
      `}</style>
    </div>
  );
};

export default ResultPage;