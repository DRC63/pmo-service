// Generic modal dialog used by the create/edit forms: a backdrop plus a centred
// panel with a title and Close button. Clicking the backdrop closes the modal;
// clicking inside the panel does not (the click is stopped from reaching the
// backdrop's onClose), so an editor can't dismiss the form by clicking its fields.
export default function Modal({ title, onClose, children }) {
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-panel" onClick={(e) => e.stopPropagation()}>
        <div className="page-header">
          <h2>{title}</h2>
          <button className="btn btn-outline btn-sm" onClick={onClose} type="button">
            Close
          </button>
        </div>
        {children}
      </div>
    </div>
  );
}
