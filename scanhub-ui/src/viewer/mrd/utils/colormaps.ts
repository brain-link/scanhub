import type { ColorPalette } from '../types';


export const plotColorPalettes: Record<string, ColorPalette> = {
  default: {
    id: 'default',
    name: 'Default',
    colors: [
      '#3B82F6', // Blue (info 500)
      '#EC4899', // Pink (joy accent)
      '#10B981', // Emerald (success 500)
      '#F59E0B', // Amber (warning 500)
      '#6366F1', // Indigo (primary 500)
      '#F43F5E', // Rose (danger-like)
      '#14B8A6', // Teal
      '#EAB308', // Yellow (bright highlight)
      '#0EA5E9', // Sky blue
    ],
  },
  viz: {
    id: 'viz',
    name: 'Viz',
    colors: [
      '#000000',
      '#0000ff',
      '#9d02d7',
      '#cd34b5',
      '#ea5f94',
      '#fa8775',
      '#ffb14e',
      '#ffd700',
    ],
  },
  matplotlib: {
    id: 'matplotlib',
    name: 'Matplotlib',
    colors: [
      '#1f77b4', // blue
      '#ff7f0e', // orange
      '#2ca02c', // green
      '#d62728', // red
      '#9467bd', // purple
      '#8c564b', // brown
      '#e377c2', // pink
      '#7f7f7f', // gray
      '#bcbd22', // olive
      '#17becf', // cyan
    ],
  },
  blue: {
    id: 'blue',
    name: 'Blue',
    colors: [
      '#3B82F6', // Blue 500 (Joy UI info main)
      '#3575dd', // Darker
      '#2f68c4',
      '#295bac',
      '#234e93',
      '#1d417a',
      '#173461',
      '#0f223d', // Nearly black with blue nuance
    ]
  },
  macarons: {
    id: 'macarons',
    name: 'Macarons',
    colors: [
      '#2ec7c9',
      '#b6a2de',
      '#5ab1ef',
      '#ffb980',
      '#d87a80',
      '#8d98b3',
      '#e5cf0d',
      '#97b552',
      '#95706d',
      '#dc69aa',
      '#07a2a4',
      '#9a7fd1',
      '#588dd5',
      '#f5994e',
      '#c05050',
      '#59678c',
      '#c9ab00',
      '#7eb00a',
      '#6f5553',
      '#c14089'
    ]
  }
};

// iterable array for UI
export const plotColorPaletteOptions: ColorPalette[] = Object.values(plotColorPalettes);
