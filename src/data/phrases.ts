import { HPhraseOption, PPhraseOption } from '../types';

export const H_PHRASES: HPhraseOption[] = [
  // Físicos
  { code: 'H220', text: 'Gas extremadamente inflamable.', category: 'Físico' },
  { code: 'H224', text: 'Líquido y vapores extremadamente inflamables.', category: 'Físico' },
  { code: 'H225', text: 'Líquido y vapores muy inflamables.', category: 'Físico' },
  { code: 'H226', text: 'Líquidos y vapores inflamables.', category: 'Físico' },
  { code: 'H228', text: 'Sólido inflamable.', category: 'Físico' },
  { code: 'H272', text: 'Puede agravar un incendio; comburente.', category: 'Físico' },
  { code: 'H280', text: 'Contiene gas a presión; peligro de explosión en caso de calentamiento.', category: 'Físico' },
  { code: 'H290', text: 'Puede ser corrosivo para los metales.', category: 'Físico' },

  // Salud
  { code: 'H301', text: 'Tóxico en caso de ingestión.', category: 'Salud' },
  { code: 'H302', text: 'Nocivo en caso de ingestión.', category: 'Salud' },
  { code: 'H304', text: 'Puede ser mortal en caso de ingestión y penetración en las vías respiratorias.', category: 'Salud' },
  { code: 'H311', text: 'Tóxico en contacto con la piel.', category: 'Salud' },
  { code: 'H312', text: 'Nocivo en contacto con la piel.', category: 'Salud' },
  { code: 'H314', text: 'Provoca quemaduras graves en la piel y lesiones oculares graves.', category: 'Salud' },
  { code: 'H315', text: 'Provoca irritación cutánea.', category: 'Salud' },
  { code: 'H317', text: 'Puede provocar una reacción alérgica en la piel.', category: 'Salud' },
  { code: 'H318', text: 'Provoca lesiones oculares graves.', category: 'Salud' },
  { code: 'H319', text: 'Provoca irritación ocular grave.', category: 'Salud' },
  { code: 'H330', text: 'Mortal en caso de inhalación.', category: 'Salud' },
  { code: 'H331', text: 'Tóxico en caso de inhalación.', category: 'Salud' },
  { code: 'H332', text: 'Nocivo si se inhala.', category: 'Salud' },
  { code: 'H335', text: 'Puede irritar las vías respiratorias.', category: 'Salud' },
  { code: 'H336', text: 'Puede provocar somnolencia o vértigo.', category: 'Salud' },
  { code: 'H350', text: 'Puede provocar cáncer.', category: 'Salud' },

  // Medio Ambiente
  { code: 'H400', text: 'Muy tóxico para los organismos acuáticos.', category: 'Medio Ambiente' },
  { code: 'H410', text: 'Muy tóxico para los organismos acuáticos, con efectos nocivos duraderos.', category: 'Medio Ambiente' },
  { code: 'H411', text: 'Tóxico para los organismos acuáticos, con efectos nocivos duraderos.', category: 'Medio Ambiente' },
  { code: 'H412', text: 'Nocivo para los organismos acuáticos, con efectos nocivos duraderos.', category: 'Medio Ambiente' },
  { code: 'H413', text: 'Puede ser nocivo para los organismos acuáticos, con efectos nocivos duraderos.', category: 'Medio Ambiente' },
];

export const P_PHRASES: PPhraseOption[] = [
  // General
  { code: 'P101', text: 'Si se necesita consejo médico, tener a mano el envase o la etiqueta.', category: 'General' },
  { code: 'P102', text: 'Mantener fuera del alcance de los niños.', category: 'General' },
  { code: 'P103', text: 'Leer la etiqueta antes del uso.', category: 'General' },

  // Prevención
  { code: 'P210', text: 'Mantener alejado de fuentes de calor, chispas, llama abierta o superficies calientes. - No fumar.', category: 'Prevención' },
  { code: 'P233', text: 'Mantener el recipiente herméticamente cerrado.', category: 'Prevención' },
  { code: 'P240', text: 'Toma de tierra y enlace equipotencial del recipiente y del equipo receptor.', category: 'Prevención' },
  { code: 'P260', text: 'No respirar el polvo/el humo/el gas/la niebla/los vapores/el aerosol.', category: 'Prevención' },
  { code: 'P261', text: 'Evitar respirar el polvo/el humo/el gas/la niebla/los vapores/el aerosol.', category: 'Prevención' },
  { code: 'P262', text: 'Evitar el contacto con los ojos, la piel o la ropa.', category: 'Prevención' },
  { code: 'P264', text: 'Lavarse las manos cuidadosamente tras la manipulación.', category: 'Prevención' },
  { code: 'P270', text: 'No comer, beber ni fumar durante su utilización.', category: 'Prevención' },
  { code: 'P271', text: 'Utilizar únicamente en exteriores o en un lugar bien ventilado.', category: 'Prevención' },
  { code: 'P273', text: 'Evitar su liberación al medio ambiente.', category: 'Prevención' },
  { code: 'P280', text: 'Usar guantes/ropa de protección/equipo de protección para los ojos/la cara.', category: 'Prevención' },

  // Respuesta
  { code: 'P301+310', text: 'EN CASO DE INGESTIÓN: Llamar inmediatamente a un CENTRO DE TOXICOLOGÍA o a un médico.', category: 'Respuesta' },
  { code: 'P301+330+331+312', text: 'EN CASO DE INGESTIÓN: enjuagarse la boca. NO provocar el vómito, Llamar inmediatamente a un CENTRO de información toxicológica o a un médico.', category: 'Respuesta' },
  { code: 'P302+352', text: 'EN CASO DE CONTACTO CON LA PIEL: Lavar con abundante agua y jabón.', category: 'Respuesta' },
  { code: 'P303+361+353', text: 'EN CASO DE CONTACTO CON LA PIEL (o el pelo): Quitarse inmediatamente las prendas contaminadas. Aclararse la piel con agua o ducharse.', category: 'Respuesta' },
  { code: 'P304+340', text: 'EN CASO DE INHALACIÓN: Transportar a la persona al aire libre y mantenerla en una posición que le facilite la respiración.', category: 'Respuesta' },
  { code: 'P305+P351+P337+P313', text: 'EN CASO DE CONTACTO CON CON LOS OJOS: Aclarar cuidadosamente con agua durante varios minutos. Si persiste la irritación ocular consultar a un médico.', category: 'Respuesta' },
  { code: 'P370+378', text: 'En caso de incendio: Utilizar dióxido de carbono (CO2), polvo químico seco o espuma para la extinción.', category: 'Respuesta' },

  // Almacenamiento
  { code: 'P403', text: 'Almacenar en un lugar bien ventilado.', category: 'Almacenamiento' },
  { code: 'P403+235', text: 'Almacenar en un lugar bien ventilado. Mantener en lugar fresco.', category: 'Almacenamiento' },
  { code: 'P405', text: 'Guardar bajo llave.', category: 'Almacenamiento' },

  // Eliminación
  { code: 'P501', text: 'Eliminar el contenido/el recipiente en una planta de eliminación de residuos autorizada.', category: 'Eliminación' },
];
