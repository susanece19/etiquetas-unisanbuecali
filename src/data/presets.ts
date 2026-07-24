import { ChemicalPreset } from '../types';

export const CHEMICAL_PRESETS: ChemicalPreset[] = [
  {
    id: 'varsol',
    name: 'VARSOL (Modelo de Referencia Colmena)',
    data: {
      productName: 'VARSOL',
      composition: 'Mezcla compleja de hidrocarburos entre C9 y C12,\nparafinas,: 79% CAS: 8052-41-3',
      signalWord: 'Atención',
      sgaPictograms: ['sga02', 'sga07'], // Inflamable, Exclamacion/Nocivo
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
    },
  },
  {
    id: 'acetona',
    name: 'ACETONA PURA (Disolvente)',
    data: {
      productName: 'ACETONA',
      composition: 'Propan-2-ona C3H6O: > 99.5%\nCAS: 67-64-1',
      signalWord: 'Peligro',
      sgaPictograms: ['sga02', 'sga07'],
      hPhrases:
        'H225 Líquido y vapores muy inflamables\nH319 Provoca irritación ocular grave\nH336 Puede provocar somnolencia o vértigo',
      pPhrases:
        'P210 Mantener alejado de fuentes de calor, chispas, llama abierta o superficies calientes. - No fumar\nP233 Mantener el recipiente herméticamente cerrado\nP305+P351+P338 EN CASO DE CONTACTO CON LOS OJOS: Aclarar cuidadosamente con agua durante varios minutos\nP403+P235 Almacenar en un lugar bien ventilado. Mantener en lugar fresco',
      unClass: 'un_clase_3',
      unCode: '1090',
      eppPictograms: ['epp_guantes', 'epp_gafas', 'epp_mascara'],
      provider: {
        name: 'QUÍMICOS Y SOLVENTES BOGOTÁ S.A.S',
        address: 'Calle 13 No. 42 - 18, Bogotá',
        phone: 'PBX: (601) 321-9876',
      },
      borderThickness: 1.5,
      fontSizeScale: 1.0,
      paddingScale: 1.0,
      labelWidth: 900,
    },
  },
  {
    id: 'acido_clorhidrico',
    name: 'ÁCIDO CLORHÍDRICO (Muriático 37%)',
    data: {
      productName: 'ÁCIDO CLORHÍDRICO',
      composition: 'Ácido Clorhídrico en solución acuosa: 37%\nCAS: 7647-01-0',
      signalWord: 'Peligro',
      sgaPictograms: ['sga05', 'sga06'], // Corrosivo, Toxicidad
      hPhrases:
        'H290 Puede ser corrosivo para los metales\nH314 Provoca quemaduras graves en la piel y lesiones oculares graves\nH331 Tóxico en caso de inhalación\nH335 Puede irritar las vías respiratorias',
      pPhrases:
        'P260 No respirar el humo/los vapores\nP280 Usar guantes, ropa de protección y equipo de protección para ojos y cara\nP301+P330+P331 EN CASO DE INGESTIÓN: Enjuagarse la boca. NO provocar el vómito\nP303+P361+P353 EN CASO DE CONTACTO CON LA PIEL: Quitarse inmediatamente la ropa contaminada. Ducharse\nP305+P351+P338 EN CASO DE CONTACTO CON LOS OJOS: Enjuagar cuidadosamente con agua',
      unClass: 'un_clase_8',
      unCode: '1789',
      eppPictograms: ['epp_guantes', 'epp_gafas', 'epp_mascara', 'epp_delantal', 'epp_botas'],
      provider: {
        name: 'INDUSTRIAS QUÍMICAS COLOMBIANAS S.A.',
        address: 'Zona Industrial Cazucá, Soacha',
        phone: 'PBX: (601) 780-1234',
      },
      borderThickness: 1.5,
      fontSizeScale: 1.0,
      paddingScale: 1.0,
      labelWidth: 900,
    },
  },
  {
    id: 'hipoclorito',
    name: 'HIPOCLORITO DE SODIO (Cloro 13%)',
    data: {
      productName: 'HIPOCLORITO DE SODIO',
      composition: 'Hipoclorito de Sodio en agua: 12.5 - 15%\nCAS: 7681-52-9',
      signalWord: 'Peligro',
      sgaPictograms: ['sga05', 'sga09'], // Corrosivo, Medio Ambiente
      hPhrases:
        'H314 Provoca quemaduras graves en la piel y lesiones oculares graves\nH400 Muy tóxico para los organismos acuáticos',
      pPhrases:
        'P273 Evitar su liberación al medio ambiente\nP280 Usar guantes y gafas de protección\nP305+P351+P338 EN CASO DE CONTACTO CON LOS OJOS: Aclarar con agua varios minutos\nP501 Eliminar el contenido según normativa vigente',
      unClass: 'un_clase_8',
      unCode: '1791',
      eppPictograms: ['epp_guantes', 'epp_gafas', 'epp_delantal'],
      provider: {
        name: 'DESINFECTANTES DE COLOMBIA LTDA',
        address: 'Carrera 68 No. 19 - 45, Bogotá',
        phone: 'PBX: (601) 412-5500',
      },
      borderThickness: 1.5,
      fontSizeScale: 1.0,
      paddingScale: 1.0,
      labelWidth: 900,
    },
  },
  {
    id: 'alcohol_70',
    name: 'ALCOHOL ETÍLICO 70%',
    data: {
      productName: 'ALCOHOL ETÍLICO 70%',
      composition: 'Etanol: 70% v/v, Agua desmineralizada: 30%\nCAS: 64-17-5',
      signalWord: 'Peligro',
      sgaPictograms: ['sga02', 'sga07'],
      hPhrases:
        'H225 Líquido y vapores muy inflamables\nH319 Provoca irritación ocular grave',
      pPhrases:
        'P210 Mantener alejado de fuentes de calor y chispas. - No fumar\nP233 Mantener el recipiente herméticamente cerrado\nP305+P351+P338 EN CASO DE CONTACTO CON LOS OJOS: Aclarar con agua cuidadosamente',
      unClass: 'un_clase_3',
      unCode: '1170',
      eppPictograms: ['epp_guantes', 'epp_gafas'],
      provider: {
        name: 'LABORATORIOS FARMAQUÍMICOS S.A.S',
        address: 'Calle 80 No. 69P - 20, Bogotá',
        phone: 'PBX: (601) 225-8899',
      },
      borderThickness: 1.5,
      fontSizeScale: 1.0,
      paddingScale: 1.0,
      labelWidth: 900,
    },
  },
  {
    id: 'thinner',
    name: 'THINNER CORRIENTE',
    data: {
      productName: 'THINNER CORRIENTE',
      composition: 'Tolueno, Xileno, Acetato de etilo, Metanol\nCAS: Mezcla Compleja',
      signalWord: 'Peligro',
      sgaPictograms: ['sga02', 'sga06', 'sga07', 'sga08'],
      hPhrases:
        'H225 Líquido y vapores muy inflamables\nH304 Puede ser mortal en caso de ingestión\nH315 Provoca irritación cutánea\nH336 Puede provocar somnolencia o vértigo\nH361 Se sospecha que perjudica la fertilidad o el feto',
      pPhrases:
        'P210 Mantener alejado de chispas y llama abierta. - No fumar\nP261 Evitar respirar vapores\nP301+P310 EN CASO DE INGESTIÓN: Llamar inmediatamente a toxicología\nP331 NO provocar el vómito',
      unClass: 'un_clase_3',
      unCode: '1263',
      eppPictograms: ['epp_guantes', 'epp_gafas', 'epp_mascara', 'epp_botas'],
      provider: {
        name: 'PINTURAS Y DISOLVENTES DEL ANDE',
        address: 'Autopista Sur Km 12, Soacha',
        phone: 'PBX: (601) 571-0011',
      },
      borderThickness: 1.5,
      fontSizeScale: 1.0,
      paddingScale: 1.0,
      labelWidth: 900,
    },
  },
];
