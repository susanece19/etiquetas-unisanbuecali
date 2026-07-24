export type SignalWord = 'Atención' | 'Peligro';

export interface SgaPictogram {
  id: string;
  code: string; // e.g. "SGA01", "SGA02"
  name: string; // e.g. "Inflamable", "Exclamación"
  description: string;
}

export interface EppPictogram {
  id: string;
  code: string;
  name: string;
  description: string;
}

export interface UnClass {
  id: string;
  code: string; // e.g. "Clase 3"
  name: string; // e.g. "Líquidos Inflamables"
  color: string; // red, yellow, green, etc.
}

export interface ProviderInfo {
  name: string;
  address: string;
  phone: string;
  email?: string;
  additionalInfo?: string;
}

export interface LabelData {
  productName: string;
  composition: string;
  signalWord: SignalWord;
  sgaPictograms: string[]; // array of sga ids/codes
  hPhrases: string; // multiline
  pPhrases: string; // multiline
  unClass: string; // un class id
  unCode: string; // e.g. "1268"
  eppPictograms: string[]; // array of epp ids/codes
  provider: ProviderInfo;
  // Customization settings
  borderThickness: number; // in px
  fontSizeScale: number; // 0.8 to 1.3
  paddingScale: number;
  labelWidth: number; // in px for canvas/print export
}

export interface ChemicalPreset {
  id: string;
  name: string;
  data: LabelData;
}

export interface HPhraseOption {
  code: string;
  text: string;
  category: 'Físico' | 'Salud' | 'Medio Ambiente';
}

export interface PPhraseOption {
  code: string;
  text: string;
  category: 'General' | 'Prevención' | 'Respuesta' | 'Almacenamiento' | 'Eliminación';
}
