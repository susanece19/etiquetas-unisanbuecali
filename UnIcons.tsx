import React, { useState } from 'react';

interface ColmenaLogoProps {
  className?: string;
  width?: number;
  height?: number;
}

export const ColmenaLogo: React.FC<ColmenaLogoProps> = ({
  className = '',
  width = 180,
  height = 55,
}) => {
  const [imgError, setImgError] = useState(false);

  if (!imgError) {
    return (
      <img
        src="/assets/logo_colmena.png"
        alt="Colmena Seguros Logo"
        className={`object-contain max-h-[60px] ${className}`}
        style={{ width: `${width}px`, height: 'auto' }}
        onError={() => setImgError(true)}
      />
    );
  }

  return (
    <div className={`flex items-center gap-2.5 select-none ${className}`}>
      {/* Honeycomb Hexagon Symbol */}
      <svg
        width={width ? width * 0.28 : 42}
        height={height ? height * 0.8 : 40}
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Top Hexagon - Yellow/Orange */}
        <path
          d="M50 10 L72 22.5 L72 47.5 L50 60 L28 47.5 L28 22.5 Z"
          fill="#F59E0B"
        />
        {/* Bottom Left Hexagon - Teal/Cyan */}
        <path
          d="M28 50 L50 62.5 L50 87.5 L28 100 L6 87.5 L6 62.5 Z"
          fill="#06B6D4"
        />
        {/* Bottom Right Hexagon - Dark Cyan */}
        <path
          d="M72 50 L94 62.5 L94 87.5 L72 100 L50 87.5 L50 62.5 Z"
          fill="#0891B2"
        />
        {/* Inner white outline accents for crisp look */}
        <path
          d="M50 10 L72 22.5 L72 47.5 L50 60 L28 47.5 L28 22.5 Z"
          stroke="#FFFFFF"
          strokeWidth="2"
        />
      </svg>

      {/* Brand Text */}
      <div className="flex flex-col justify-center leading-tight">
        <span
          className="font-bold tracking-tight text-cyan-600 font-sans"
          style={{ fontSize: `${(width || 180) * 0.13}px` }}
        >
          Colmena
        </span>
        <span
          className="text-gray-500 font-medium tracking-wide"
          style={{ fontSize: `${(width || 180) * 0.075}px` }}
        >
          Seguros
        </span>
      </div>
    </div>
  );
};
