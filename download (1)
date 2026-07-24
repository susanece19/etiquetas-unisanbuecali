import React, { useState } from 'react';

export interface UnClassInfo {
  id: string;
  code: string;
  name: string;
  description: string;
  bgHex: string;
  textHex: string;
}

export const UN_CLASS_LIST: UnClassInfo[] = [
  { id: 'un_clase_1.1', code: 'Clase 1.1', name: 'Explosivos 1.1', description: 'Riesgo de explosión en masa', bgHex: '#D97706', textHex: '#FFFFFF' },
  { id: 'un_clase_2.1', code: 'Clase 2.1', name: 'Gases Inflamables', description: 'Gases inflamables', bgHex: '#DC2626', textHex: '#FFFFFF' },
  { id: 'un_clase_2.2', code: 'Clase 2.2', name: 'Gases No Inflamables / No Tóxicos', description: 'Gases comprimidos', bgHex: '#16A34A', textHex: '#FFFFFF' },
  { id: 'un_clase_2.3', code: 'Clase 2.3', name: 'Gases Tóxicos', description: 'Gases tóxicos por inhalación', bgHex: '#FFFFFF', textHex: '#000000' },
  { id: 'un_clase_3', code: 'Clase 3', name: 'Líquidos Inflamables', description: 'Líquidos con punto de inflamación bajo', bgHex: '#DC2626', textHex: '#FFFFFF' },
  { id: 'un_clase_4.1', code: 'Clase 4.1', name: 'Sólidos Inflamables', description: 'Sólidos inflamables o autorreactivos', bgHex: '#DC2626', textHex: '#FFFFFF' },
  { id: 'un_clase_5.1', code: 'Clase 5.1', name: 'Sustancias Comburentes', description: 'Oxidantes', bgHex: '#EAB308', textHex: '#000000' },
  { id: 'un_clase_6.1', code: 'Clase 6.1', name: 'Sustancias Tóxicas', description: 'Tóxicos por ingestión, piel o inhalación', bgHex: '#FFFFFF', textHex: '#000000' },
  { id: 'un_clase_7', code: 'Clase 7', name: 'Material Radiactivo', description: 'Sustancias radiactivas', bgHex: '#EAB308', textHex: '#000000' },
  { id: 'un_clase_8', code: 'Clase 8', name: 'Sustancias Corrosivas', description: 'Corrosivos para la piel y metales', bgHex: '#1E293B', textHex: '#FFFFFF' },
  { id: 'un_clase_9', code: 'Clase 9', name: 'Sustancias Peligrosas Varias', description: 'Otros riesgos de transporte', bgHex: '#FFFFFF', textHex: '#000000' },
];

interface UnIconProps {
  id: string;
  size?: number;
  className?: string;
}

export const UnIcon: React.FC<UnIconProps> = ({ id, size = 56, className = '' }) => {
  const [imgError, setImgError] = useState(false);

  const getUnAssetUrl = (rawId: string) => {
    let clean = rawId.toUpperCase().replace('UN_', '').replace('CLASE_', '');
    if (!clean) clean = '3';
    // Match against known file formats
    if (clean === '3') return '/assets/un/CLASE_3.png';
    if (clean === '7') return '/assets/un/CLASE_7.png';
    if (clean === '8') return '/assets/un/CLASE_8.png';
    if (clean === '9') return '/assets/un/CLASE_9.png';
    if (clean.startsWith('1')) return `/assets/un/CLASE_${clean.includes('.') ? clean : '1.1'}.png`;
    if (clean.startsWith('2')) return `/assets/un/CLASE_${clean.includes('.') ? clean : '2.1'}.png`;
    if (clean.startsWith('4')) return `/assets/un/CLASE_${clean.includes('.') ? clean : '4.1'}.png`;
    if (clean.startsWith('5')) return `/assets/un/CLASE_${clean.includes('.') ? clean : '5.1'}.png`;
    if (clean.startsWith('6')) return `/assets/un/CLASE_${clean.includes('.') ? clean : '6.1'}.png`;
    return `/assets/un/CLASE_${clean}.png`;
  };

  const assetUrl = getUnAssetUrl(id);
  const info = UN_CLASS_LIST.find((u) => u.id === id || u.id.endsWith(id.toLowerCase())) || UN_CLASS_LIST[4];

  if (!imgError) {
    return (
      <div
        className={`relative flex items-center justify-center select-none ${className}`}
        style={{ width: size, height: size }}
        title={`${info.code}: ${info.name}`}
      >
        <img
          src={assetUrl}
          alt={`UN ${id}`}
          className="w-full h-full object-contain"
          onError={() => setImgError(true)}
        />
      </div>
    );
  }

  // Fallback SVG render
  return (
    <div
      className={`relative flex items-center justify-center select-none ${className}`}
      style={{ width: size, height: size }}
      title={`${info.code}: ${info.name}`}
    >
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <polygon
          points="50,4 96,50 50,96 4,50"
          fill={info.bgHex}
          stroke={info.textHex === '#000000' ? '#000000' : '#FFFFFF'}
          strokeWidth="3"
        />
        <g transform="translate(50, 50) scale(0.8)">
          <path
            d="M0 12 C -10 12, -15 2, -15 -8 C -15 -20, -7 -28, -1 -34 C 0 -26, 4 -18, 8 -14 C 4 -22, -2 -28, 0 -35 C 9 -27, 16 -16, 16 -4 C 16 8, 10 12, 0 12 Z"
            fill={info.textHex}
          />
          <text x="0" y="32" textAnchor="middle" fill={info.textHex} fontSize="22" fontWeight="bold" fontFamily="sans-serif">
            {info.code.replace('Clase ', '')}
          </text>
        </g>
      </svg>
    </div>
  );
};
