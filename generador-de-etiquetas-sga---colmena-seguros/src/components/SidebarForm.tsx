import React, { useState } from 'react';
import { LabelData, SignalWord } from '../types';
import { SGA_LIST, SgaIcon } from './SgaIcons';
import { EPP_LIST, EppIcon } from './EppIcons';
import { UN_CLASS_LIST, UnIcon } from './UnIcons';
import { CHEMICAL_PRESETS } from '../data/presets';
import { PhraseSelectorModal } from './PhraseSelectorModal';
import {
  FlaskConical,
  BookOpen,
  Sliders,
  Sparkles,
  Info,
  ShieldAlert,
  Truck,
  Building2,
  ListPlus,
  RotateCcw,
} from 'lucide-react';

interface SidebarFormProps {
  data: LabelData;
  onChange: (newData: LabelData) => void;
  onLoadPreset: (presetId: string) => void;
}

export const SidebarForm: React.FC<SidebarFormProps> = ({
  data,
  onChange,
  onLoadPreset,
}) => {
  const [activeTab, setActiveTab] = useState<'content' | 'appearance'>('content');
  const [phraseModalType, setPhraseModalType] = useState<'H' | 'P' | null>(null);

  const updateField = <K extends keyof LabelData>(field: K, value: LabelData[K]) => {
    onChange({ ...data, [field]: value });
  };

  const updateProviderField = (key: keyof LabelData['provider'], value: string) => {
    onChange({
      ...data,
      provider: {
        ...data.provider,
        [key]: value,
      },
    });
  };

  const toggleSga = (id: string) => {
    const current = [...data.sgaPictograms];
    const updated = current.includes(id)
      ? current.filter((x) => x !== id)
      : [...current, id];
    updateField('sgaPictograms', updated);
  };

  const toggleEpp = (id: string) => {
    const current = [...data.eppPictograms];
    const updated = current.includes(id)
      ? current.filter((x) => x !== id)
      : [...current, id];
    updateField('eppPictograms', updated);
  };

  return (
    <div className="w-full lg:w-[420px] bg-slate-900 border-r border-slate-800 flex flex-col h-full text-slate-200 select-none overflow-hidden shrink-0">
      {/* Sidebar Header & Presets Bar */}
      <div className="p-4 border-b border-slate-800 bg-slate-950/60">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-cyan-600/20 text-cyan-400 rounded-lg">
              <FlaskConical className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-bold text-sm text-slate-100 leading-tight">
                Panel de Configuración
              </h2>
              <p className="text-[11px] text-slate-400">Etiqueta Colmena Seguros SGA</p>
            </div>
          </div>

          {/* Tab buttons */}
          <div className="flex p-0.5 bg-slate-800/80 rounded-lg text-xs font-medium">
            <button
              onClick={() => setActiveTab('content')}
              className={`px-2.5 py-1 rounded-md transition-all ${
                activeTab === 'content'
                  ? 'bg-cyan-600 text-white shadow-xs'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Datos
            </button>
            <button
              onClick={() => setActiveTab('appearance')}
              className={`px-2.5 py-1 rounded-md transition-all ${
                activeTab === 'appearance'
                  ? 'bg-cyan-600 text-white shadow-xs'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Diseño
            </button>
          </div>
        </div>

        {/* Quick Presets Dropdown */}
        <div className="bg-slate-800/60 p-2 rounded-lg border border-slate-700/50 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-amber-400 shrink-0" />
          <span className="text-xs text-slate-300 font-medium whitespace-nowrap">Plantilla:</span>
          <select
            onChange={(e) => onLoadPreset(e.target.value)}
            className="w-full bg-slate-900 text-slate-100 text-xs py-1 px-2 rounded border border-slate-700 focus:outline-hidden focus:border-cyan-500 font-medium cursor-pointer"
          >
            <option value="">-- Cargar reactivo químico predeterminado --</option>
            {CHEMICAL_PRESETS.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Form Fields Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-5">
        {activeTab === 'content' ? (
          <>
            {/* 1. Nombre del Producto & Composición */}
            <div className="space-y-3 bg-slate-800/40 p-3.5 rounded-xl border border-slate-800">
              <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider">
                <Info className="w-3.5 h-3.5" /> 1. Identificación y Composición
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Nombre del Producto / Reactivo *
                </label>
                <input
                  type="text"
                  value={data.productName}
                  onChange={(e) => updateField('productName', e.target.value)}
                  placeholder="Ej: VARSOL, ACETONA..."
                  className="w-full px-3 py-1.5 text-sm bg-slate-900 text-slate-100 rounded-lg border border-slate-700 focus:border-cyan-500 focus:outline-hidden font-bold tracking-wide"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Composición Química (Multilínea)
                </label>
                <textarea
                  rows={2}
                  value={data.composition}
                  onChange={(e) => updateField('composition', e.target.value)}
                  placeholder="Ej: Mezcla compleja de hidrocarburos entre C9 y C12, CAS: 8052-41-3..."
                  className="w-full px-3 py-1.5 text-xs bg-slate-900 text-slate-100 rounded-lg border border-slate-700 focus:border-cyan-500 focus:outline-hidden font-mono resize-y"
                />
              </div>
            </div>

            {/* 2. Palabra de Advertencia */}
            <div className="space-y-2 bg-slate-800/40 p-3.5 rounded-xl border border-slate-800">
              <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider">
                <ShieldAlert className="w-3.5 h-3.5" /> 2. Palabra de Advertencia
              </div>

              <div className="grid grid-cols-2 gap-2">
                {(['Atención', 'Peligro'] as SignalWord[]).map((word) => (
                  <button
                    key={word}
                    type="button"
                    onClick={() => updateField('signalWord', word)}
                    className={`py-2 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
                      data.signalWord === word
                        ? word === 'Peligro'
                          ? 'bg-red-600 text-white shadow-md'
                          : 'bg-amber-600 text-white shadow-md'
                        : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-700'
                    }`}
                  >
                    {word}
                  </button>
                ))}
              </div>
            </div>

            {/* 3. Pictogramas SGA / GHS */}
            <div className="space-y-2 bg-slate-800/40 p-3.5 rounded-xl border border-slate-800">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider">
                  <ShieldAlert className="w-3.5 h-3.5" /> 3. Pictogramas SGA / GHS ({data.sgaPictograms.length})
                </span>
                <span className="text-[10px] text-slate-400">Haz clic para seleccionar</span>
              </div>

              <div className="grid grid-cols-3 gap-2 pt-1">
                {SGA_LIST.map((sga) => {
                  const selected = data.sgaPictograms.includes(sga.id);
                  return (
                    <button
                      key={sga.id}
                      type="button"
                      onClick={() => toggleSga(sga.id)}
                      className={`p-1.5 rounded-lg border transition-all flex flex-col items-center justify-center text-center ${
                        selected
                          ? 'border-red-500 bg-red-950/40 ring-1 ring-red-500'
                          : 'border-slate-800 bg-slate-900/60 hover:border-slate-700'
                      }`}
                      title={sga.description}
                    >
                      <SgaIcon id={sga.id} size={42} />
                      <span className="text-[10px] font-medium text-slate-300 mt-1 line-clamp-1">
                        {sga.name}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* 4. Frases H & Frases P */}
            <div className="space-y-3 bg-slate-800/40 p-3.5 rounded-xl border border-slate-800">
              {/* Frases H */}
              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5" /> Frases H (Indicaciones Peligro)
                  </label>
                  <button
                    type="button"
                    onClick={() => setPhraseModalType('H')}
                    className="text-[11px] font-medium text-cyan-400 hover:text-cyan-300 flex items-center gap-1 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/50"
                  >
                    <ListPlus className="w-3 h-3" /> Catálogo H
                  </button>
                </div>
                <textarea
                  rows={3}
                  value={data.hPhrases}
                  onChange={(e) => updateField('hPhrases', e.target.value)}
                  placeholder="H226 Líquidos y vapores inflamables&#10;H302 Nocivo en caso de ingestión..."
                  className="w-full px-3 py-1.5 text-xs bg-slate-900 text-slate-100 rounded-lg border border-slate-700 focus:border-cyan-500 focus:outline-hidden font-mono resize-y leading-relaxed"
                />
              </div>

              {/* Frases P */}
              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5" /> Frases P (Consejos Prudencia)
                  </label>
                  <button
                    type="button"
                    onClick={() => setPhraseModalType('P')}
                    className="text-[11px] font-medium text-cyan-400 hover:text-cyan-300 flex items-center gap-1 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/50"
                  >
                    <ListPlus className="w-3 h-3" /> Catálogo P
                  </button>
                </div>
                <textarea
                  rows={4}
                  value={data.pPhrases}
                  onChange={(e) => updateField('pPhrases', e.target.value)}
                  placeholder="P102 Mantener fuera del alcance de los niños&#10;P210 Mantener alejado de fuentes de calor..."
                  className="w-full px-3 py-1.5 text-xs bg-slate-900 text-slate-100 rounded-lg border border-slate-700 focus:border-cyan-500 focus:outline-hidden font-mono resize-y leading-relaxed"
                />
              </div>
            </div>

            {/* 5. Transporte UN & EPP */}
            <div className="space-y-3 bg-slate-800/40 p-3.5 rounded-xl border border-slate-800">
              <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider">
                <Truck className="w-3.5 h-3.5" /> 5. Transporte UN & EPP
              </div>

              {/* UN Class & Code */}
              <div className="grid grid-cols-12 gap-2 items-center">
                <div className="col-span-7">
                  <label className="block text-xs font-medium text-slate-300 mb-1">
                    Clase de Transporte UN
                  </label>
                  <select
                    value={data.unClass}
                    onChange={(e) => updateField('unClass', e.target.value)}
                    className="w-full bg-slate-900 text-slate-100 text-xs py-1.5 px-2 rounded-lg border border-slate-700 focus:border-cyan-500 focus:outline-hidden font-medium"
                  >
                    {UN_CLASS_LIST.map((u) => (
                      <option key={u.id} value={u.id}>
                        {u.code}: {u.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="col-span-5">
                  <label className="block text-xs font-medium text-slate-300 mb-1">
                    Número UN
                  </label>
                  <input
                    type="text"
                    value={data.unCode}
                    onChange={(e) => updateField('unCode', e.target.value)}
                    placeholder="Ej: 1268"
                    className="w-full px-2.5 py-1.5 text-xs font-bold bg-slate-900 text-slate-100 rounded-lg border border-slate-700 focus:border-cyan-500 focus:outline-hidden text-center"
                  />
                </div>
              </div>

              {/* EPP Selection */}
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Pictogramas EPP Recomendados ({data.eppPictograms.length})
                </label>
                <div className="grid grid-cols-4 gap-2 pt-1">
                  {EPP_LIST.map((epp) => {
                    const selected = data.eppPictograms.includes(epp.id);
                    return (
                      <button
                        key={epp.id}
                        type="button"
                        onClick={() => toggleEpp(epp.id)}
                        className={`p-1.5 rounded-lg border transition-all flex flex-col items-center justify-center ${
                          selected
                            ? 'border-blue-500 bg-blue-950/50 ring-1 ring-blue-500'
                            : 'border-slate-800 bg-slate-900/60 hover:border-slate-700'
                        }`}
                        title={epp.name}
                      >
                        <EppIcon id={epp.id} size={36} />
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* 6. Información del Proveedor */}
            <div className="space-y-2 bg-slate-800/40 p-3.5 rounded-xl border border-slate-800">
              <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider">
                <Building2 className="w-3.5 h-3.5" /> 6. Información del Proveedor
              </div>

              <div>
                <label className="block text-[11px] text-slate-400 mb-0.5">Empresa</label>
                <input
                  type="text"
                  value={data.provider.name}
                  onChange={(e) => updateProviderField('name', e.target.value)}
                  className="w-full px-2.5 py-1 text-xs bg-slate-900 text-slate-100 rounded border border-slate-700 focus:border-cyan-500 focus:outline-hidden font-medium"
                />
              </div>

              <div>
                <label className="block text-[11px] text-slate-400 mb-0.5">Dirección / Ciudad</label>
                <input
                  type="text"
                  value={data.provider.address}
                  onChange={(e) => updateProviderField('address', e.target.value)}
                  className="w-full px-2.5 py-1 text-xs bg-slate-900 text-slate-100 rounded border border-slate-700 focus:border-cyan-500 focus:outline-hidden"
                />
              </div>

              <div>
                <label className="block text-[11px] text-slate-400 mb-0.5">Teléfonos / Contacto</label>
                <input
                  type="text"
                  value={data.provider.phone}
                  onChange={(e) => updateProviderField('phone', e.target.value)}
                  className="w-full px-2.5 py-1 text-xs bg-slate-900 text-slate-100 rounded border border-slate-700 focus:border-cyan-500 focus:outline-hidden"
                />
              </div>
            </div>
          </>
        ) : (
          /* Appearance & Dimensions Tab */
          <div className="space-y-4 bg-slate-800/40 p-4 rounded-xl border border-slate-800">
            <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-wider mb-2">
              <Sliders className="w-4 h-4" /> Dimensiones y Escala
            </div>

            {/* Label Width */}
            <div>
              <div className="flex justify-between text-xs text-slate-300 mb-1">
                <span>Ancho de Etiqueta</span>
                <span className="font-mono font-bold">{data.labelWidth} px</span>
              </div>
              <input
                type="range"
                min="650"
                max="1200"
                step="25"
                value={data.labelWidth}
                onChange={(e) => updateField('labelWidth', Number(e.target.value))}
                className="w-full accent-cyan-500 cursor-pointer"
              />
            </div>

            {/* Font Size Scale */}
            <div>
              <div className="flex justify-between text-xs text-slate-300 mb-1">
                <span>Escala de Fuente</span>
                <span className="font-mono font-bold">{(data.fontSizeScale * 100).toFixed(0)}%</span>
              </div>
              <input
                type="range"
                min="0.8"
                max="1.3"
                step="0.05"
                value={data.fontSizeScale}
                onChange={(e) => updateField('fontSizeScale', Number(e.target.value))}
                className="w-full accent-cyan-500 cursor-pointer"
              />
            </div>

            {/* Border Thickness */}
            <div>
              <div className="flex justify-between text-xs text-slate-300 mb-1">
                <span>Grosor de Bordes</span>
                <span className="font-mono font-bold">{data.borderThickness} px</span>
              </div>
              <input
                type="range"
                min="1"
                max="3"
                step="0.5"
                value={data.borderThickness}
                onChange={(e) => updateField('borderThickness', Number(e.target.value))}
                className="w-full accent-cyan-500 cursor-pointer"
              />
            </div>

            <div className="pt-4 border-t border-slate-800">
              <button
                type="button"
                onClick={() => onLoadPreset('varsol')}
                className="w-full py-2 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg border border-slate-700 flex items-center justify-center gap-1.5 transition-colors"
              >
                <RotateCcw className="w-3.5 h-3.5" /> Restablecer a Modelo VARSOL original
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Phrase Selector Modal */}
      {phraseModalType && (
        <PhraseSelectorModal
          type={phraseModalType}
          isOpen={!!phraseModalType}
          onClose={() => setPhraseModalType(null)}
          currentText={phraseModalType === 'H' ? data.hPhrases : data.pPhrases}
          onSelectPhrases={(text) => {
            if (phraseModalType === 'H') updateField('hPhrases', text);
            else updateField('pPhrases', text);
          }}
        />
      )}
    </div>
  );
};
