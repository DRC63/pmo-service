// Reusable data table shared by the list pages. `columns` describe each column
// ({ key, label, numeric?, render? }) and `rows` are the data. A column's optional
// render(row) lets a cell show a component (a badge, an allocation bar) instead of
// a raw value. Shows an empty-state message when there are no rows, and makes rows
// clickable when onRowClick is supplied (used to open a detail page).
export default function DataTable({ columns, rows, emptyMessage = 'No data yet.', rowKey = 'id', onRowClick }) {
  if (!rows || rows.length === 0) {
    return (
      <div className="data-table-wrap">
        <div className="data-table-empty">{emptyMessage}</div>
      </div>
    );
  }

  return (
    <div className="data-table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key} className={col.numeric ? 'numeric' : undefined}>
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr
              key={row[rowKey]}
              onClick={onRowClick ? () => onRowClick(row) : undefined}
              style={onRowClick ? { cursor: 'pointer' } : undefined}
            >
              {columns.map((col) => (
                <td key={col.key} className={col.numeric ? 'numeric' : undefined}>
                  {col.render ? col.render(row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
