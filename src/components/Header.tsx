import React from 'react';
import {
  Download,
  Printer,
  Copy,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Check,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';

interface HeaderProps {
  onExportPng: (scaleMultiplier?: number) => void;
  onPrint: () => void;
  onCopyPng: () => void;
  zoomScale: number;
  setZoomScale: (scale: number | ((prev: number) => number)) => void;
  isExporting: boolean;
  copied: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  onExportPng,
  onPrint,
  onCopyPng,
  zoomScale,
  setZoomScale,
  isExporting,
  copied,
}) => {
  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 px-4 flex items-center justify-between text-slate-100 shrink-0 z-10 shadow-md">
      {/* Title */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 to-amber-500 flex items-center justify-center text-white shadow-md">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div>
          <h1 className="font-extrabold text-base tracking-tight leading-tight text-white flex items-center gap-2">
            Generador de Etiquetas SGA
            <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800">
              Colmena Seguros
            </span>
          </h1>
          <p className="text-xs text-slate-400">
            Generación de imagen PNG en alta resolución (Cumple NTC 4435 / SGA / GHS)
          </p>
        </div>
      </div>

      {/* Controls & Export Action Buttons */}
      <div className="flex items-center gap-3">
        {/* Zoom controls */}
        <div className="hidden md:flex items-center bg-slate-800/80 rounded-lg p-1 border border-slate-700/60 text-xs">
          <button
            onClick={() => setZoomScale((prev) => Math.max(0.4, prev - 0.1))}
            title="Reducir zoom"
            className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <span className="px-2 font-mono font-medium text-slate-200">
            {(zoomScale * 100).toFixed(0)}%
          </span>
          <button
            onClick={() => setZoomScale((prev) => Math.min(1.5, prev + 0.1))}
            title="Aumentar zoom"
            className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-700 rounded transition-colors"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={() => setZoomScale(0.85)}
            title="Ajustar a pantalla"
            className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-700 rounded transition-colors border-l border-slate-700 ml-1"
          >
            <Maximize2 className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Copy PNG Button */}
        <button
          onClick={onCopyPng}
          disabled={isExporting}
          className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-lg border border-slate-700 transition-colors"
        >
          {copied ? (
            <>
              <Check className="w-4 h-4 text-emerald-400" /> ¡Copiado!
            </>
          ) : (
            <>
              <Copy className="w-4 h-4" /> Copiar Imagen
            </>
          )}
        </button>

        {/* Print Label Button */}
        <button
          onClick={onPrint}
          className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-200 bg-slate-800 hover:bg-slate-700 rounded-lg border border-slate-700 transition-colors"
        >
          <Printer className="w-4 h-4" /> Imprimir
        </button>

        {/* Primary Action: Download PNG */}
        <div className="flex items-center">
          <button
            onClick={() => onExportPng(2)}
            disabled={isExporting}
            className="flex items-center gap-2 px-4 py-2 text-xs font-bold text-white bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 active:scale-98 rounded-lg shadow-md shadow-cyan-950 transition-all cursor-pointer disabled:opacity-50"
          >
            <Download className="w-4 h-4" />
            {isExporting ? 'Generando PNG...' : 'Descargar Etiqueta PNG (HD)'}
          </button>
        </div>
      </div>
    </header>
  );
};
