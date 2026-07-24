import React, { useState } from 'react';

export interface EppIconInfo {
  id: string;
  code: string;
  name: string;
  description: string;
}

export const EPP_LIST: EppIconInfo[] = [
  { id: 'epp_botas', code: 'EPP01', name: 'Botas de Seguridad', description: 'Usar botas o calzado de seguridad impermeable' },
  { id: 'epp_careta', code: 'EPP02', name: 'Careta Facial', description: 'Usar pantalla o careta de protección facial' },
  { id: 'epp_gafas', code: 'EPP03', name: 'Protección Ocular', description: 'Usar gafas o monogafas de seguridad' },
  { id: 'epp_guantes', code: 'EPP04', name: 'Guantes de Protección', description: 'Usar guantes de seguridad química' },
  { id: 'epp_mascara', code: 'EPP05', name: 'Respirador / Mascarilla', description: 'Usar mascarilla o respirador' },
  { id: 'epp_mascara_gas', code: 'EPP06', name: 'Mascarilla para Gases', description: 'Usar mascarilla con filtro para gases y vapores' },
  { id: 'epp_prenda', code: 'EPP07', name: 'Prenda de Protección', description: 'Usar traje o delantal de protección química' },
];

interface EppIconProps {
  id: string;
  size?: number;
  className?: string;
}

export const EppIcon: React.FC<EppIconProps> = ({ id, size = 48, className = '' }) => {
  const [imgError, setImgError] = useState(false);

  // Map id to assets/epp/*.png file name
  const getEppAssetUrl = (rawId: string) => {
    const lower = rawId.toLowerCase();
    if (lower.includes('bota')) return '/assets/epp/BOTAS.png';
    if (lower.includes('careta')) return '/assets/epp/CARETA.png';
    if (lower.includes('gafa') || lower.includes('ojo')) return '/assets/epp/GAFAS.png';
    if (lower.includes('guante')) return '/assets/epp/GUANTES.png';
    if (lower.includes('gas')) return '/assets/epp/MASCARILLA GAS.png';
    if (lower.includes('mascar') || lower.includes('respirad')) return '/assets/epp/MASCARILLA.png';
    return '/assets/epp/PRENDA.png';
  };

  const assetUrl = getEppAssetUrl(id);

  if (!imgError) {
    return (
      <div
        className={`relative flex items-center justify-center rounded-full overflow-hidden bg-[#0055A5] p-1 shadow-xs border border-white ${className}`}
        style={{ width: size, height: size }}
        title={EPP_LIST.find((e) => e.id === id)?.name || id}
      >
        <img
          src={assetUrl}
          alt={`EPP ${id}`}
          className="w-full h-full object-contain filter drop-shadow-xs"
          onError={() => setImgError(true)}
        />
      </div>
    );
  }

  // Fallback SVG symbol
  const renderSymbol = () => {
    switch (id) {
      case 'epp_guantes':
      case 'epp_delantal':
        return (
          <g transform="translate(50, 50) scale(0.85)">
            <path
              d="M-12,-26 L12,-26 L16,-12 L24,-4 L18,24 L-18,24 L-24,-4 L-16,-12 Z"
              fill="#FFFFFF"
            />
            <circle cx="0" cy="-20" r="4" fill="#0055A5" />
          </g>
        );

      case 'epp_gafas':
        return (
          <g transform="translate(50, 50) scale(0.85)">
            <rect x="-32" y="-12" width="28" height="24" rx="8" stroke="#FFFFFF" strokeWidth="5" fill="none" />
            <rect x="4" y="-12" width="28" height="24" rx="8" stroke="#FFFFFF" strokeWidth="5" fill="none" />
            <path d="M-4,-4 C-2,-8 2,-8 4,-4" stroke="#FFFFFF" strokeWidth="5" fill="none" />
            <path d="M-32,-4 L-42,-12" stroke="#FFFFFF" strokeWidth="4" strokeLinecap="round" />
            <path d="M32,-4 L42,-12" stroke="#FFFFFF" strokeWidth="4" strokeLinecap="round" />
          </g>
        );

      case 'epp_mascara':
        return (
          <g transform="translate(50, 50) scale(0.85)">
            <path d="M-28,8 C-28,-12 -12,-22 0,-22 C12,-22 28,-12 28,8 C28,18 14,24 0,24 C-14,24 -28,18 -28,8 Z" fill="#FFFFFF" />
            <circle cx="-16" cy="6" r="6" fill="#0055A5" />
            <circle cx="16" cy="6" r="6" fill="#0055A5" />
            <path d="M-28,0 L-40,-10 M28,0 L40,-10 M-28,12 L-38,18 M28,12 L38,18" stroke="#FFFFFF" strokeWidth="3" />
          </g>
        );

      case 'epp_botas':
        return (
          <g transform="translate(50, 50) scale(0.82)">
            <path
              d="M-12,-28 L6,-28 C8,-28 10,-26 10,-24 L10,0 C12,0 20,4 28,10 C34,14 34,22 28,22 L-12,22 C-16,22 -18,20 -18,16 L-18,-22 C-18,-26 -16,-28 -12,-28 Z"
              fill="#FFFFFF"
            />
            <line x1="-18" y1="18" x2="30" y2="18" stroke="#0055A5" strokeWidth="2" />
          </g>
        );

      case 'epp_careta':
        return (
          <g transform="translate(50, 50) scale(0.85)">
            <path d="M-26,-12 C-26,-22 26,-22 26,-12" stroke="#FFFFFF" strokeWidth="5" fill="none" />
            <path
              d="M-24,-10 C-24,20 -12,28 0,28 C12,28 24,20 24,-10 Z"
              fill="#FFFFFF"
              fillOpacity="0.85"
              stroke="#FFFFFF"
              strokeWidth="2"
            />
          </g>
        );

      default:
        return (
          <g transform="translate(50, 50) scale(0.85)">
            <circle cx="0" cy="0" r="20" fill="#FFFFFF" />
          </g>
        );
    }
  };

  return (
    <div
      className={`relative flex items-center justify-center select-none ${className}`}
      style={{ width: size, height: size }}
      title={EPP_LIST.find((e) => e.id === id)?.name || id}
    >
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="50" cy="50" r="46" fill="#0055A5" stroke="#FFFFFF" strokeWidth="2" />
        {renderSymbol()}
      </svg>
    </div>
  );
};
