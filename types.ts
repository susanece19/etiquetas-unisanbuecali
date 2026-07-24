import React, { useState } from 'react';
import { H_PHRASES, P_PHRASES } from '../data/phrases';
import { X, Search, Plus, Check } from 'lucide-react';

interface PhraseSelectorModalProps {
  type: 'H' | 'P';
  isOpen: boolean;
  onClose: () => void;
  onSelectPhrases: (phrasesText: string) => void;
  currentText: string;
}

export const PhraseSelectorModal: React.FC<PhraseSelectorModalProps> = ({
  type,
  isOpen,
  onClose,
  onSelectPhrases,
  currentText,
}) => {
  const [search, setSearch] = useState('');
  const [selectedCodes, setSelectedCodes] = useState<string[]>([]);

  if (!isOpen) return null;

  const phraseList = type === 'H' ? H_PHRASES : P_PHRASES;

  const filtered = phraseList.filter(
    (p) =>
      p.code.toLowerCase().includes(search.toLowerCase()) ||
      p.text.toLowerCase().includes(search.toLowerCase()) ||
      p.category.toLowerCase().includes(search.toLowerCase())
  );

  const toggleSelect = (code: string) => {
    setSelectedCodes((prev) =>
      prev.includes(code) ? prev.filter((c) => c !== code) : [...prev, code]
    );
  };

  const handleApply = () => {
    const selectedObj = phraseList.filter((p) => selectedCodes.includes(p.code));
    const newLines = selectedObj.map((p) => `${p.code} ${p.text}`);
    
    // Combine with current text cleanly
    const existing = currentText.trim();
    const result = existing ? `${existing}\n${newLines.join('\n')}` : newLines.join('\n');

    onSelectPhrases(result);
    setSelectedCodes([]);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-2xl w-full max-w-2xl max-h-[85vh] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
          <div>
            <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100 flex items-center gap-2">
              Catálogo de {type === 'H' ? 'Indicaciones de Peligro (Frases H)' : 'Consejos de Prudencia (Frases P)'}
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Selecciona las frases estándar para agregarlas automáticamente a tu etiqueta.
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-200/50 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search Input */}
        <div className="p-3 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
            <input
              type="text"
              placeholder={`Buscar por código (ej. ${type === 'H' ? 'H226' : 'P210'}), texto o categoría...`}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-sm bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-lg border border-transparent focus:border-cyan-500 focus:outline-hidden"
            />
          </div>
        </div>

        {/* Phrase List */}
        <div className="p-3 overflow-y-auto flex-1 space-y-2">
          {filtered.length > 0 ? (
            filtered.map((item) => {
              const isSelected = selectedCodes.includes(item.code);
              return (
                <div
                  key={item.code}
                  onClick={() => toggleSelect(item.code)}
                  className={`p-3 rounded-lg border text-sm cursor-pointer transition-all flex items-start gap-3 ${
                    isSelected
                      ? 'border-cyan-500 bg-cyan-50/70 dark:bg-cyan-950/40 text-cyan-900 dark:text-cyan-100'
                      : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300'
                  }`}
                >
                  <div
                    className={`mt-0.5 w-5 h-5 rounded flex items-center justify-center text-xs shrink-0 ${
                      isSelected
                        ? 'bg-cyan-600 text-white'
                        : 'border border-slate-300 dark:border-slate-600'
                    }`}
                  >
                    {isSelected && <Check className="w-3.5 h-3.5" />}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="font-bold text-slate-900 dark:text-slate-100 font-mono text-xs px-1.5 py-0.5 bg-slate-200 dark:bg-slate-800 rounded">
                        {item.code}
                      </span>
                      <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800/80 px-2 py-0.5 rounded-full">
                        {item.category}
                      </span>
                    </div>
                    <p className="text-xs leading-relaxed text-slate-700 dark:text-slate-300">
                      {item.text}
                    </p>
                  </div>
                </div>
              );
            })
          ) : (
            <div className="p-8 text-center text-slate-400 text-sm">
              No se encontraron frases coincidentes.
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50 flex items-center justify-between">
          <span className="text-xs text-slate-500 dark:text-slate-400">
            {selectedCodes.length} frase(s) seleccionada(s)
          </span>
          <div className="flex gap-2">
            <button
              onClick={onClose}
              className="px-3 py-1.5 text-xs font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-lg"
            >
              Cancelar
            </button>
            <button
              onClick={handleApply}
              disabled={selectedCodes.length === 0}
              className="px-4 py-1.5 text-xs font-bold text-white bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg shadow-xs flex items-center gap-1.5 transition-colors"
            >
              <Plus className="w-3.5 h-3.5" /> Agregar Seleccionadas
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
