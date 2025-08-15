import { useMemo } from 'react';
export type Layout = '1x1' | '1x3' | '2x2' | '2x1' | 'L-2v' | 'R-2v';

export function useViewportGrid(layout: Layout) {
  return useMemo(() => {
    switch (layout) {
      case '1x3': return { rows: 1, cols: 3, areas: ['a b c'] };
      case '2x2': return { rows: 2, cols: 2, areas: ['a b', 'c d'] };
      case '2x1': return { rows: 2, cols: 1, areas: ['a', 'b'] };
      case 'L-2v': return { rows: 2, cols: 2, areas: ['a b', 'a c'] };
      case 'R-2v': return { rows: 2, cols: 2, areas: ['a b', 'c b'] };
      default:    return { rows: 1, cols: 1, areas: ['a'] };
    }
  }, [layout]);
}
