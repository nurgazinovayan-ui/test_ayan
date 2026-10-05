import { createContext, useContext } from 'react';

/** Palette + rhythm of one generated piece (the preview and its two variants). */
export type HandVariant = {
  bg: string;
  ink: string;
  muted: string;
  a1: string;
  a2: string;
  capInk: string;
  grid: number;
  layout: 'left' | 'center' | 'right';
  speed: number;
  stagger: number;
};

/**
 * One art direction of the hand-drawn cut. The script, timing and layout are shared; a look only
 * changes colours, lettering and how the pencil behaves.
 */
export type Look = {
  id: string;
  name: string;
  dark: boolean;
  bg: string;
  /** fill of boxes (prompt field, cards, preview) */
  paper: string;
  ink: string;
  ink2: string;
  ink3: string;
  /** outline colour of boxes */
  line: string;
  a1: string;
  a2: string;
  aSoft: string;
  gradient: string;
  font: string;
  weight: number;
  /** font of the big FLOW letters inside the piece */
  flowFont: string;
  flowWeight: number;
  /** optical size correction for the FLOW letters (fonts differ a lot in width) */
  flowScale: number;
  upper: boolean;
  tracking: string;
  /** multipliers for the pencil */
  stroke: number;
  rough: number;
  fillStyle: 'hachure' | 'zigzag' | 'cross-hatch' | 'solid' | 'dots';
  /** 0 = plain pencil, >0 = neon glow radius */
  glow: number;
  /** background helpers */
  bgGlow: number;
  bgGrid: number;
  grainBlend: 'overlay' | 'multiply' | 'soft-light';
  grain: number;
  variants: [HandVariant, HandVariant, HandVariant];
};

const NIGHT: HandVariant = {
  bg: '#0E0F14',
  ink: '#F4F4F6',
  muted: 'rgba(244,244,246,0.5)',
  a1: '#3B7BFF',
  a2: '#A78BFA',
  capInk: '#FFFFFF',
  grid: 0.16,
  layout: 'left',
  speed: 1,
  stagger: 5,
};
const PAPER_V: HandVariant = {
  bg: '#EFECE4',
  ink: '#16161C',
  muted: 'rgba(22,22,28,0.55)',
  a1: '#6D5BF5',
  a2: '#3B7BFF',
  capInk: '#FFFFFF',
  grid: 0.18,
  layout: 'center',
  speed: 1.3,
  stagger: 3,
};
const BLUEPRINT_V: HandVariant = {
  bg: '#0D1C4F',
  ink: '#EEF2FF',
  muted: 'rgba(238,242,255,0.55)',
  a1: '#A78BFA',
  a2: '#7FB0FF',
  capInk: '#0D1C4F',
  grid: 0.22,
  layout: 'right',
  speed: 0.8,
  stagger: 8,
};

const grad = (a: string, b: string) => `linear-gradient(90deg, ${a} 0%, ${b} 100%)`;

export const LOOKS: Record<string, Look> = {
  // 1 — chalk on night (the storyboard)
  chalk: {
    id: 'chalk',
    name: 'Мел',
    dark: true,
    bg: '#09090B',
    paper: '#0F0F13',
    ink: '#FAFAFA',
    ink2: 'rgba(250,250,250,0.62)',
    ink3: 'rgba(250,250,250,0.38)',
    line: 'rgba(250,250,250,0.82)',
    a1: '#3B7BFF',
    a2: '#A78BFA',
    aSoft: '#7FA8FF',
    gradient: grad('#7FA8FF', '#A78BFA'),
    font: "'Caveat', cursive",
    weight: 700,
    flowFont: "'Caveat', cursive",
    flowWeight: 700,
    flowScale: 1,
    upper: false,
    tracking: '0',
    stroke: 1,
    rough: 1,
    fillStyle: 'hachure',
    glow: 0,
    bgGlow: 1,
    bgGrid: 0,
    grainBlend: 'overlay',
    grain: 0.5,
    variants: [NIGHT, PAPER_V, BLUEPRINT_V],
  },
  // 2 — graphite and markers in a sketchbook
  sketchbook: {
    id: 'sketchbook',
    name: 'Скетчбук',
    dark: false,
    bg: '#EFEBE1',
    paper: '#F8F5EE',
    ink: '#1A1A21',
    ink2: 'rgba(26,26,33,0.66)',
    ink3: 'rgba(26,26,33,0.42)',
    line: 'rgba(26,26,33,0.78)',
    a1: '#2F6BFF',
    a2: '#7C5CF0',
    aSoft: '#2F6BFF',
    gradient: grad('#2F6BFF', '#7C5CF0'),
    font: "'Neucha', cursive",
    weight: 400,
    flowFont: "'Neucha', cursive",
    flowWeight: 400,
    flowScale: 0.9,
    upper: false,
    tracking: '0',
    stroke: 1.1,
    rough: 1.1,
    fillStyle: 'hachure',
    glow: 0,
    bgGlow: 0.25,
    bgGrid: 0,
    grainBlend: 'multiply',
    grain: 0.9,
    variants: [
      { ...PAPER_V, bg: '#F8F5EE', a1: '#2F6BFF', a2: '#7C5CF0', layout: 'left', speed: 1, stagger: 5 },
      { ...NIGHT, layout: 'center', speed: 1.3, stagger: 3 },
      BLUEPRINT_V,
    ],
  },
  // 3 — white pencil on a blueprint
  blueprint: {
    id: 'blueprint',
    name: 'Блюпринт',
    dark: true,
    bg: '#0A1A4A',
    paper: '#0C1F57',
    ink: '#EEF2FF',
    ink2: 'rgba(238,242,255,0.7)',
    ink3: 'rgba(238,242,255,0.45)',
    line: 'rgba(238,242,255,0.85)',
    a1: '#7FB0FF',
    a2: '#C4B5FD',
    aSoft: '#9CC2FF',
    gradient: grad('#9CC2FF', '#C4B5FD'),
    font: "'Amatic SC', cursive",
    weight: 700,
    flowFont: "'Amatic SC', cursive",
    flowWeight: 700,
    flowScale: 1.3,
    upper: false,
    tracking: '0.02em',
    stroke: 0.9,
    rough: 0.8,
    fillStyle: 'cross-hatch',
    glow: 0,
    bgGlow: 0.5,
    bgGrid: 0.09,
    grainBlend: 'overlay',
    grain: 0.5,
    variants: [
      { ...BLUEPRINT_V, bg: '#0C1F57', layout: 'left', speed: 1, stagger: 5, a1: '#7FB0FF', a2: '#C4B5FD' },
      { ...NIGHT, layout: 'center', speed: 1.3, stagger: 3 },
      { ...PAPER_V, layout: 'right', speed: 0.8, stagger: 8 },
    ],
  },
  // 4 — glowing doodles on black
  neon: {
    id: 'neon',
    name: 'Неон-дудл',
    dark: true,
    bg: '#060608',
    paper: '#0B0B10',
    ink: '#F5F3FF',
    ink2: 'rgba(245,243,255,0.66)',
    ink3: 'rgba(245,243,255,0.4)',
    line: '#8FB3FF',
    a1: '#4D8BFF',
    a2: '#B794FF',
    aSoft: '#8FB3FF',
    gradient: grad('#6FA0FF', '#C3A6FF'),
    font: "'Pangolin', cursive",
    weight: 400,
    flowFont: "'Pangolin', cursive",
    flowWeight: 400,
    flowScale: 0.78,
    upper: false,
    tracking: '0',
    stroke: 1.1,
    rough: 0.9,
    fillStyle: 'zigzag',
    glow: 6,
    bgGlow: 0.6,
    bgGrid: 0,
    grainBlend: 'overlay',
    grain: 0.45,
    variants: [
      { ...NIGHT, bg: '#0B0B10', a1: '#4D8BFF', a2: '#B794FF' },
      { ...NIGHT, bg: '#120A24', a1: '#B794FF', a2: '#FF8AD8', layout: 'center', speed: 1.3, stagger: 3 },
      { ...BLUEPRINT_V, bg: '#071433', a1: '#5EE1FF', a2: '#7FB0FF', capInk: '#071433' },
    ],
  },
  // 5 — fat marker poster
  marker: {
    id: 'marker',
    name: 'Маркер-постер',
    dark: true,
    bg: '#09090B',
    paper: '#101014',
    ink: '#FAFAFA',
    ink2: 'rgba(250,250,250,0.66)',
    ink3: 'rgba(250,250,250,0.4)',
    line: '#FAFAFA',
    a1: '#3B7BFF',
    a2: '#A78BFA',
    aSoft: '#7FA8FF',
    gradient: grad('#7FA8FF', '#A78BFA'),
    font: "'Caveat', cursive",
    weight: 700,
    flowFont: "'Rubik Doodle Shadow', cursive",
    flowWeight: 400,
    flowScale: 0.74,
    upper: false,
    tracking: '0',
    stroke: 2.1,
    rough: 1.9,
    fillStyle: 'hachure',
    glow: 0,
    bgGlow: 0.7,
    bgGrid: 0,
    grainBlend: 'overlay',
    grain: 0.6,
    variants: [NIGHT, PAPER_V, BLUEPRINT_V],
  },
};

export const LookContext = createContext<Look>(LOOKS.chalk);
export const useLook = () => useContext(LookContext);
