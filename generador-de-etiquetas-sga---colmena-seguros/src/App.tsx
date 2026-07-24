import React, { useState, useRef, useEffect } from 'react';
import { LabelData } from './types';
import { CHEMICAL_PRESETS } from './data/presets';
import { LabelPreview } from './components/LabelPreview';
import { SidebarForm } from './components/SidebarForm';
import { Header } from './components/Header';
import { toPng, toBlob } from 'html-to-image';
import confetti from 'canvas-confetti';
import { Sparkles, Eye, Info, CheckCircle2, FileImage } from 'lucide-react';

export default function App() {
  // Initialize state with default VARSOL preset (matches Colmena Seguros reference model)
  const defaultVarsol = CHEMICAL_PRESETS.find((p) => p.id === 'varsol')?.data || {
    productName: 'VARSOL',
    composition: 'Mezcla compleja de hidrocarburos entre C9 y C12,\nparafinas,: 79% CAS: 8052-41-3',
    signalWord: 'Atención',
    sgaPictograms: ['sga02', 'sga07'],
    hPhrases:
      'H226 Líquidos y vapores inflamables\nH302 Nocivo en caso de ingestión\nH312 Nocivo en contacto con la piel\nH332 Nocivo si se inhala\nH413 Puede ser nocivo para los organismos acuáticos, con efectos nocivos duraderos',
    pPhrases:
      'P102 Mantener fuera del alcance de los niños\nP210 Mantener alejado de fuentes de calor, chispas, llama abierta o superficies calientes. - No fumar\nP262 Evitar el contacto con los ojos, la piel o la ropa\nP403 Almacenar en un lugar bien ventilado\nP301+330+331+312 EN CASO DE INGESTIÓN: enjuagarse la boca. NO provocar el vómito,Llamar inmediatamente a un CENTRO de información toxicológica o a un médico\nP305+P351+P337+P313 EN CASO DE CONTACTO CON LOS OJOS: Aclarar cuidadosamente con agua durante varios minutos. Si persiste la irritación ocular consultar a un médico\nP303+361+353 EN CASO DE CONTACTO CON LA PIEL (o el pelo): Quitarse inmediatamente las prendas contaminadas. Aclararse la piel con agua o ducharse',
    unClass: 'un_clase_3',
    unCode: '1268',
    eppPictograms: ['epp_guantes', 'epp_gafas', 'epp_mascara', 'epp_botas'],
    provider: {
      name: 'CONSTELACIÓN INDUSTRIAL DEL ASEO S.A.S',
      address: '59 No. 5A - 77/85 Bogotá, Colombia',
      phone: 'PBX: (1) 4069777 - 3132526836',
    },
    borderThickness: 1.5,
    fontSizeScale: 1.0,
    paddingScale: 1.0,
    labelWidth: 900,
  };

  const [labelData, setLabelData] = useState<LabelData>(defaultVarsol);
  const [zoomScale, setZoomScale] = useState<number>(0.85);
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  const labelCanvasRef = useRef<HTMLDivElement>(null);

  // Responsive zoom adjustment on window resize
  useEffect(() => {
    const handleResize = () => {
      const screenWidth = window.innerWidth;
      if (screenWidth < 768) setZoomScale(0.38);
      else if (screenWidth < 1024) setZoomScale(0.55);
      else if (screenWidth < 1400) setZoomScale(0.75);
      else setZoomScale(0.85);
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Load a pre-configured chemical preset
  const handleLoadPreset = (presetId: string) => {
    const preset = CHEMICAL_PRESETS.find((p) => p.id === presetId);
    if (preset) {
      setLabelData(preset.data);
    }
  };

  // Export Label to PNG format
  const handleExportPng = async (pixelRatio = 2) => {
    if (!labelCanvasRef.current) return;

    try {
      setIsExporting(true);

      // Render crisp HD image with 2x pixel ratio for print sharpness
      const dataUrl = await toPng(labelCanvasRef.current, {
        pixelRatio,
        cacheBust: true,
        backgroundColor: '#FFFFFF',
      });

      // Trigger automatic file download
      const cleanName = (labelData.productName || 'ETIQUETA_SGA').trim().replace(/[\s\W]+/g, '_');
      const filename = `Etiqueta_SGA_Colmena_${cleanName}.png`;

      const link = document.createElement('a');
      link.download = filename;
      link.href = dataUrl;
      link.click();

      // Trigger celebratory confetti effect
      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.8 },
      });
    } catch (err) {
      console.error('Error al exportar PNG:', err);
      alert('Ocurrió un error al generar la imagen PNG. Por favor reintenta.');
    } finally {
      setIsExporting(false);
    }
  };

  // Copy PNG image directly to clipboard
  const handleCopyPng = async () => {
    if (!labelCanvasRef.current) return;

    try {
      setIsExporting(true);
      const blob = await toBlob(labelCanvasRef.current, {
        pixelRatio: 2,
        backgroundColor: '#FFFFFF',
      });

      if (blob) {
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': blob }),
        ]);
        setCopied(true);
        setTimeout(() => setCopied(false), 2500);
      }
    } catch (err) {
      console.error('Error al copiar imagen:', err);
      alert('Tu navegador no admite copiar directamente imágenes al portapapeles. Usa la opción Descargar PNG.');
    } finally {
      setIsExporting(false);
    }
  };

  // Trigger Browser Print Dialog
  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-slate-950 font-sans">
      {/* Top Header Controls */}
      <Header
        onExportPng={handleExportPng}
        onPrint={handlePrint}
        onCopyPng={handleCopyPng}
        zoomScale={zoomScale}
        setZoomScale={setZoomScale}
        isExporting={isExporting}
        copied={copied}
      />

      {/* Main Content Workspace: Sidebar + Canvas Preview */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* Left Sidebar Input Controls */}
        <SidebarForm
          data={labelData}
          onChange={setLabelData}
          onLoadPreset={handleLoadPreset}
        />

        {/* Right Label Preview Canvas Stage */}
        <main className="flex-1 bg-slate-900/60 p-4 md:p-8 flex flex-col items-center justify-start overflow-auto relative">
          {/* Top Canvas Bar Indicator */}
          <div className="w-full max-w-4xl flex items-center justify-between mb-4 text-xs text-slate-400 border-b border-slate-800 pb-2 shrink-0">
            <div className="flex items-center gap-2">
              <Eye className="w-4 h-4 text-cyan-400" />
              <span className="font-medium text-slate-300">
                Vista Previa en Tiempo Real (Modelo Colmena Seguros)
              </span>
            </div>
            <div className="flex items-center gap-3 text-[11px]">
              <span className="flex items-center gap-1 text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/60">
                <CheckCircle2 className="w-3 h-3" /> Redimensionamiento Dinámico Activo
              </span>
              <span className="text-slate-500 font-mono">
                {labelData.labelWidth}px × Auto-Alto
              </span>
            </div>
          </div>

          {/* Centered Scrollable Canvas Wrapper */}
          <div className="flex-1 flex items-center justify-center min-h-[550px] w-full p-4 overflow-auto">
            <LabelPreview
              ref={labelCanvasRef}
              data={labelData}
              scale={zoomScale}
              className="transition-transform duration-200"
            />
          </div>

          {/* Quick Info Footer Bar */}
          <div className="w-full max-w-4xl mt-4 p-3 bg-slate-900/90 border border-slate-800 rounded-xl text-xs text-slate-400 flex flex-wrap items-center justify-between gap-2 shrink-0">
            <div className="flex items-center gap-2">
              <FileImage className="w-4 h-4 text-cyan-400" />
              <span>
                Formato de salida: <strong className="text-slate-200">PNG HD (300 DPI)</strong> listo para impresión o ficha técnica SDS/FDS.
              </span>
            </div>
            <div className="text-[11px] text-slate-500">
              Cumple especificaciones SGA NTC 4435 / Colmena Seguros
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
