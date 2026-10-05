import React from 'react';
export function Pagination({ currentPage, totalPages }: { currentPage: number, totalPages: number }) {
  return <div>Page {currentPage} of {totalPages}</div>;
}
