import React, { useState } from 'react';

export interface SgaIconInfo {
  id: string;
  code: string;
  name: string;
  description: string;
}

export const SGA_LIST: SgaIconInfo[] = [
  { id: 'sga01', code: 'SGA01', name: 'Explosivo', description: 'Explosivo / Bomba explotando' },
  { id: 'sga02', code: 'SGA02', name: 'Inflamable', description: 'Líquidos, sólidos o gases inflamables' },
  { id: 'sga03', code: 'SGA03', name: 'Comburente', description: 'Llama sobre círculo / Oxidante' },
  { id: 'sga04', code: 'SGA04', name: 'Gas a presión', description: 'Cilindro de gas' },
  { id: 'sga05', code: 'SGA05', name: 'Corrosivo', description: 'Corrosión cutánea o metales' },
  { id: 'sga06', code: 'SGA06', name: 'Toxicidad Aguda', description: 'Calavera y tibias cruzadas' },
  { id: 'sga07', code: 'SGA07', name: 'Nocivo / Exclamación', description: 'Peligro para la salud humana / Irritante' },
  { id: 'sga08', code: 'SGA08', name: 'Peligro para la salud', description: 'Mutagenicidad, carcinogenicidad' },
  { id: 'sga09', code: 'SGA09', name: 'Medio Ambiente', description: 'Peligro acuático' },
];

interface SgaIconProps {
  id: string;
  size?: number;
  className?: string;
}

export const SgaIcon: React.FC<SgaIconProps> = ({ id, size = 64, className = '' }) => {
  const [imgError, setImgError] = useState(false);

  // Normalize id to asset filename e.g. sga02 -> GHS02.png
  const getAssetFilename = (rawId: string) => {
    const digits = rawId.match(/\d+/)?.[0] || '02';
    const formatted = digits.padStart(2, '0');
    return `/assets/sga/GHS${formatted}.png`;
  };

  const assetUrl = getAssetFilename(id);

  if (!imgError) {
    return (
      <div
        className={`relative flex items-center justify-center select-none ${className}`}
        style={{ width: size, height: size }}
      >
        <img
          src={assetUrl}
          alt={`Pictograma SGA ${id}`}
          className="w-full h-full object-contain"
          onError={() => setImgError(true)}
        />
      </div>
    );
  }

  // Fallback SVG rendering
  const renderSymbol = () => {
    switch (id) {
      case 'sga01':
        return (
          <g transform="translate(50, 50) scale(0.75)">
            <circle cx="0" cy="10" r="14" fill="#000" />
            <path d="M-15,-10 L-25,-25 M0,-18 L0,-32 M15,-10 L25,-25 M-20,0 L-34,-5 M20,0 L34,-5" stroke="#000" strokeWidth="4" strokeLinecap="round" />
            <path d="M-12,5 L-20,20 M12,5 L20,20 M0,20 L0,30" stroke="#000" strokeWidth="4" strokeLinecap="round" />
            <circle cx="-5" cy="-8" r="3" fill="#000" />
            <circle cx="8" cy="-5" r="2" fill="#000" />
          </g>
        );

      case 'sga02':
        return (
          <g transform="translate(50, 50) scale(0.8)">
            <path
              d="M0 25 C -15 25, -22 10, -22 -5 C -22 -22, -10 -32, -2 -38 C -1 -28, 4 -20, 10 -15 C 6 -26, -2 -34, 0 -42 C 12 -32, 22 -18, 22 -3 C 22 12, 14 25, 0 25 Z"
              fill="#000"
            />
            <path
              d="M-2 22 C -8 22, -12 14, -12 5 C -12 -5, -4 -12, -1 -18 C 3 -12, 8 -6, 8 5 C 8 14, 4 22, -2 22 Z"
              fill="#FFF"
            />
            <path
              d="M-2 20 C -5 20, -7 15, -7 8 C -7 2, -2 -3, -1 -7 C 1 -3, 4 1, 4 8 C 4 15, 1 20, -2 20 Z"
              fill="#000"
            />
          </g>
        );

      case 'sga03':
        return (
          <g transform="translate(50, 50) scale(0.8)">
            <circle cx="0" cy="8" r="15" stroke="#000" strokeWidth="5" fill="none" />
            <path
              d="M0 -2 C -10 -2, -14 -12, -14 -20 C -14 -32, -5 -38, 0 -42 C 5 -38, 14 -32, 14 -20 C 14 -12, 10 -2, 0 -2 Z"
              fill="#000"
            />
            <path
              d="M0 -5 C -5 -5, -8 -12, -8 -18 C -8 -25, -2 -28, 0 -32 C 2 -28, 8 -25, 8 -18 C 8 -12, 5 -5, 0 -5 Z"
              fill="#FFF"
            />
          </g>
        );

      case 'sga04':
        return (
          <g transform="translate(50, 50) scale(0.85)">
            <rect x="-12" y="-28" width="24" height="52" rx="12" fill="#000" />
            <rect x="-5" y="-36" width="10" height="10" fill="#000" />
            <rect x="-8" y="-38" width="16" height="4" rx="1" fill="#000" />
            <rect x="-8" y="-15" width="16" height="26" fill="#FFF" />
          </g>
        );

      case 'sga05':
        return (
          <g transform="translate(50, 50) scale(0.8)">
            <path d="M-30,-28 L-18,-16 L-24,-10 L-36,-22 Z" fill="#000" />
            <path d="M30,-28 L18,-16 L24,-10 L36,-22 Z" fill="#000" />
            <path d="M-18,-14 C-15,-5 -12,5 -12,12" stroke="#000" strokeWidth="4" strokeDasharray="3,3" />
            <path d="M18,-14 C15,-5 12,5 12,12" stroke="#000" strokeWidth="4" strokeDasharray="3,3" />
            <rect x="-28" y="10" width="22" height="10" fill="#000" />
            <path d="M-22,10 C-20,15 -14,15 -12,10" fill="#FFF" />
            <path d="M8,18 C12,18 16,16 22,16 C26,16 30,18 30,22 L10,22 Z" fill="#000" />
            <path d="M12,10 C14,15 18,15 20,10" fill="#FFF" />
          </g>
        );

      case 'sga06':
        return (
          <g transform="translate(50, 50) scale(0.82)">
            <path d="M-25,-25 L25,25 M25,-25 L-25,25" stroke="#000" strokeWidth="7" strokeLinecap="round" />
            <circle cx="-25" cy="-25" r="4" fill="#000" />
            <circle cx="25" cy="25" r="4" fill="#000" />
            <circle cx="25" cy="-25" r="4" fill="#000" />
            <circle cx="-25" cy="25" r="4" fill="#000" />
            <path d="M-18,-12 C-18,-28 18,-28 18,-12 C18,0 12,5 12,12 L-12,12 C-12,5 -18,0 -18,-12 Z" fill="#000" />
            <ellipse cx="-7" cy="-10" rx="4" ry="6" fill="#FFF" />
            <ellipse cx="7" cy="-10" rx="4" ry="6" fill="#FFF" />
            <polygon points="0,-3 -3,3 3,3" fill="#FFF" />
            <path d="M-8,12 L-8,7 M-3,12 L-3,7 M2,12 L2,7 M7,12 L7,7" stroke="#FFF" strokeWidth="2" />
          </g>
        );

      case 'sga07':
        return (
          <g transform="translate(50, 50) scale(0.85)">
            <path d="M-6,-28 L6,-28 L4,2 L-4,2 Z" fill="#000" />
            <circle cx="0" cy="16" r="6" fill="#000" />
          </g>
        );

      case 'sga08':
        return (
          <g transform="translate(50, 50) scale(0.78)">
            <circle cx="0" cy="-24" r="9" fill="#000" />
            <path d="M-22,18 L-18,-8 C-14,-14 14,-14 18,-8 L22,18 Z" fill="#000" />
            <polygon points="0,-12 3,-4 11,-4 5,2 7,10 0,5 -7,10 -5,2 -11,-4 -3,-4" fill="#FFF" />
          </g>
        );

      case 'sga09':
        return (
          <g transform="translate(50, 50) scale(0.78)">
            <path d="M-12,12 L-12,-18 M-12,-10 L-22,-20 M-12,-2 L-2, -12 M-12,4 L-22,-4" stroke="#000" strokeWidth="4" strokeLinecap="round" />
            <path d="M0,16 C8,8 20,12 26,16 C20,20 8,24 0,16 Z" fill="#000" />
            <polygon points="26,16 32,10 32,22" fill="#000" />
            <circle cx="6" cy="14" r="1.5" fill="#FFF" />
            <path d="M-30,22 L30,22" stroke="#000" strokeWidth="3" />
          </g>
        );

      default:
        return null;
    }
  };

  return (
    <div
      className={`relative flex items-center justify-center select-none ${className}`}
      style={{ width: size, height: size }}
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
          fill="#FFFFFF"
          stroke="#DC2626"
          strokeWidth="7"
          strokeLinejoin="miter"
        />
        {renderSymbol()}
      </svg>
    </div>
  );
};
