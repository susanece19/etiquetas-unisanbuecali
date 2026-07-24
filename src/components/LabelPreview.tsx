import React, { forwardRef } from 'react';
import { LabelData } from '../types';
import { ColmenaLogo } from './ColmenaLogo';
import { SgaIcon } from './SgaIcons';
import { EppIcon } from './EppIcons';
import { UnIcon } from './UnIcons';

interface LabelPreviewProps {
  data: LabelData;
  scale?: number; // Visual scale for on-screen preview
  className?: string;
}

export const LabelPreview = forwardRef<HTMLDivElement, LabelPreviewProps>(
  ({ data, scale = 1, className = '' }, ref) => {
    const {
      productName,
      composition,
      signalWord,
      sgaPictograms,
      hPhrases,
      pPhrases,
      unClass,
      unCode,
      eppPictograms,
      provider,
      borderThickness = 1.5,
      fontSizeScale = 1.0,
      labelWidth = 900,
    } = data;

    // Helper to format multiline text safely
    const hLines = hPhrases.split('\n').filter((l) => l.trim().length > 0);
    const pLines = pPhrases.split('\n').filter((l) => l.trim().length > 0);
    const compositionLines = composition.split('\n').filter((l) => l.trim().length > 0);

    // Font size modifiers based on fontSizeScale
    const baseTitleSize = 13 * fontSizeScale;
    const baseTextSize = 11 * fontSizeScale;
    const productNameSize = 28 * fontSizeScale;
    const signalWordSize = 16 * fontSizeScale;

    return (
      <div
        className={`inline-block origin-top select-none ${className}`}
        style={{
          transform: scale !== 1 ? `scale(${scale})` : undefined,
          transformOrigin: 'top center',
        }}
      >
        {/* Printable & Exportable Label Canvas */}
        <div
          ref={ref}
          id="colmena-label-canvas"
          className="bg-white text-black font-sans box-border relative shadow-lg print:shadow-none"
          style={{
            width: `${labelWidth}px`,
            minHeight: '520px',
            border: `${borderThickness * 2}px solid #000000`,
            padding: '0px',
            color: '#000000',
            backgroundColor: '#FFFFFF',
          }}
        >
          {/* ==================== ROW 1: HEADER (LOGO | PRODUCT NAME | COMPOSITION) ==================== */}
          <div
            className="grid grid-cols-12 border-b border-black"
            style={{ borderBottomWidth: `${borderThickness}px` }}
          >
            {/* Logo Colmena */}
            <div
              className="col-span-3 p-3 flex items-center justify-center border-r border-black"
              style={{ borderRightWidth: `${borderThickness}px` }}
            >
              <ColmenaLogo width={170} />
            </div>

            {/* Product Name (Center) */}
            <div
              className="col-span-6 p-4 flex items-center justify-center text-center font-bold tracking-wider border-r border-black uppercase"
              style={{
                borderRightWidth: `${borderThickness}px`,
                fontSize: `${productNameSize}px`,
                lineHeight: 1.1,
              }}
            >
              {productName || 'NOMBRE DEL PRODUCTO'}
            </div>

            {/* Composition (Right) */}
            <div className="col-span-3 flex flex-col justify-start">
              <div
                className="font-bold text-center py-1.5 px-2 bg-gray-50 border-b border-black uppercase tracking-tight"
                style={{
                  fontSize: `${baseTitleSize}px`,
                  borderBottomWidth: `${borderThickness}px`,
                }}
              >
                Composición
              </div>
              <div
                className="p-2.5 text-center flex-1 flex flex-col justify-center leading-tight"
                style={{ fontSize: `${baseTextSize * 0.9}px` }}
              >
                {compositionLines.length > 0 ? (
                  compositionLines.map((line, idx) => (
                    <div key={idx} className="my-0.5">
                      {line}
                    </div>
                  ))
                ) : (
                  <span className="text-gray-400 italic">Sin datos de composición</span>
                )}
              </div>
            </div>
          </div>

          {/* ==================== ROW 2: PALABRA DE ADVERTENCIA ==================== */}
          <div
            className="grid grid-cols-12 border-b border-black"
            style={{ borderBottomWidth: `${borderThickness}px` }}
          >
            <div
              className="col-span-3 p-2 font-bold text-center border-r border-black flex items-center justify-center"
              style={{
                borderRightWidth: `${borderThickness}px`,
                fontSize: `${baseTitleSize}px`,
              }}
            >
              Palabra de Advertencia
            </div>
            <div
              className={`col-span-9 p-2 font-bold text-center flex items-center justify-center uppercase tracking-wide ${
                signalWord === 'Peligro' ? 'text-red-700' : 'text-amber-700'
              }`}
              style={{ fontSize: `${signalWordSize}px` }}
            >
              {signalWord || 'ATENCIÓN'}
            </div>
          </div>

          {/* ==================== ROWS 3 & 4: SGA (LEFT COLUMN) | FRASES H & P (RIGHT COLUMN) ==================== */}
          <div
            className="grid grid-cols-12 border-b border-black flex-1"
            style={{ borderBottomWidth: `${borderThickness}px` }}
          >
            {/* SGA Pictograms Column (Spans full height of Rows 3 & 4) */}
            <div
              className="col-span-3 border-r border-black flex flex-col justify-start"
              style={{ borderRightWidth: `${borderThickness}px` }}
            >
              <div
                className="font-bold text-center py-1.5 px-2 border-b border-black uppercase tracking-tight bg-gray-50"
                style={{
                  fontSize: `${baseTitleSize}px`,
                  borderBottomWidth: `${borderThickness}px`,
                }}
              >
                Pictogramas SGA
              </div>
              <div className="p-3 flex-1 flex flex-wrap items-center justify-center gap-3 min-h-[180px]">
                {sgaPictograms.length > 0 ? (
                  sgaPictograms.map((sgaId) => (
                    <SgaIcon key={sgaId} id={sgaId} size={sgaPictograms.length > 2 ? 56 : 68} />
                  ))
                ) : (
                  <span className="text-gray-400 text-xs text-center italic">
                    Sin pictogramas
                  </span>
                )}
              </div>
            </div>

            {/* Right Column: Frases H (Top) and Frases P (Bottom) */}
            <div className="col-span-9 flex flex-col">
              {/* Top: Indicaciones de peligro (Frases H) */}
              <div
                className="flex flex-col border-b border-black"
                style={{ borderBottomWidth: `${borderThickness}px` }}
              >
                <div
                  className="font-bold text-center py-1.5 px-2 border-b border-black uppercase tracking-tight bg-gray-50"
                  style={{
                    fontSize: `${baseTitleSize}px`,
                    borderBottomWidth: `${borderThickness}px`,
                  }}
                >
                  Indicaciones de peligro (Frases H)
                </div>
                <div
                  className="p-3 flex-1 flex flex-col justify-center items-center text-center leading-snug space-y-1 min-h-[80px]"
                  style={{ fontSize: `${baseTextSize}px` }}
                >
                  {hLines.length > 0 ? (
                    hLines.map((line, idx) => (
                      <div key={idx} className="max-w-[95%]">
                        {line}
                      </div>
                    ))
                  ) : (
                    <span className="text-gray-400 italic">Sin indicaciones H</span>
                  )}
                </div>
              </div>

              {/* Bottom: Consejos de prudencia (Frases P) */}
              <div className="flex flex-col flex-1">
                <div
                  className="font-bold text-center py-1.5 px-2 border-b border-black uppercase tracking-tight bg-gray-50"
                  style={{
                    fontSize: `${baseTitleSize}px`,
                    borderBottomWidth: `${borderThickness}px`,
                  }}
                >
                  Consejos de prudencia (Frases P)
                </div>
                <div
                  className="p-3 flex-1 flex flex-col justify-center items-center text-center leading-normal space-y-1 min-h-[100px]"
                  style={{ fontSize: `${baseTextSize * 0.92}px` }}
                >
                  {pLines.length > 0 ? (
                    pLines.map((line, idx) => (
                      <div key={idx} className="max-w-[96%]">
                        {line}
                      </div>
                    ))
                  ) : (
                    <span className="text-gray-400 italic">Sin consejos de prudencia P</span>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* ==================== ROW 5: UN | EPP | PROVEEDOR ==================== */}
          <div className="grid grid-cols-12 min-h-[120px]">
            {/* Column 1: UN Transport */}
            <div
              className="col-span-3 border-r border-black flex flex-col justify-between"
              style={{ borderRightWidth: `${borderThickness}px` }}
            >
              <div
                className="font-bold text-center py-1.5 px-2 border-b border-black uppercase tracking-tight bg-gray-50"
                style={{
                  fontSize: `${baseTitleSize * 0.9}px`,
                  borderBottomWidth: `${borderThickness}px`,
                }}
              >
                Pictogramas Naciones Unidas
              </div>
              <div className="p-2 flex-1 flex flex-col items-center justify-center gap-1.5">
                <UnIcon id={unClass} size={50} />
                <div
                  className="flex items-center justify-between w-full px-2 pt-1 font-bold text-xs"
                  style={{ fontSize: `${baseTextSize * 0.9}px` }}
                >
                  <span>Identificacion UN</span>
                  <span className="text-sm font-extrabold">{unCode || '1268'}</span>
                </div>
              </div>
            </div>

            {/* Column 2: EPP / PPE Icons */}
            <div
              className="col-span-5 border-r border-black flex flex-col justify-between"
              style={{ borderRightWidth: `${borderThickness}px` }}
            >
              <div
                className="font-bold text-center py-1.5 px-2 border-b border-black uppercase tracking-tight bg-gray-50"
                style={{
                  fontSize: `${baseTitleSize * 0.9}px`,
                  borderBottomWidth: `${borderThickness}px`,
                }}
              >
                EPP (Elementos Proteccion Personal a usar)
              </div>
              <div className="p-2 flex-1 flex items-center justify-center flex-wrap gap-2.5">
                {eppPictograms.length > 0 ? (
                  eppPictograms.map((eppId) => <EppIcon key={eppId} id={eppId} size={42} />)
                ) : (
                  <span className="text-gray-400 text-xs italic">Sin EPP asignados</span>
                )}
              </div>
            </div>

            {/* Column 3: Provider Information */}
            <div className="col-span-4 flex flex-col justify-between">
              <div
                className="font-bold text-center py-1.5 px-2 border-b border-black uppercase tracking-tight bg-gray-50"
                style={{
                  fontSize: `${baseTitleSize * 0.9}px`,
                  borderBottomWidth: `${borderThickness}px`,
                }}
              >
                Información del proveedor
              </div>
              <div
                className="p-2.5 flex-1 flex flex-col items-center justify-center text-center leading-tight font-sans space-y-1 uppercase"
                style={{ fontSize: `${baseTextSize * 0.92}px` }}
              >
                <div className="font-bold text-gray-900">{provider.name || 'PROVEEDOR'}</div>
                <div className="text-gray-800">{provider.address}</div>
                <div className="text-gray-800 font-medium">{provider.phone}</div>
                {provider.email && <div className="text-gray-700 font-normal">{provider.email}</div>}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
);

LabelPreview.displayName = 'LabelPreview';
