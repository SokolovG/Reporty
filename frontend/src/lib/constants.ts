export const RECORD_STATUS = {
    OPEN: 'OPEN',
    CLOSED: 'CLOSED'
};

export const STATUS_STYLES = {
    [RECORD_STATUS.OPEN]: 'bg-emerald-100 text-emerald-700',
    [RECORD_STATUS.CLOSED]: 'bg-slate-100 text-slate-700'
};

export const STATUS_LABELS = {
    [RECORD_STATUS.OPEN]: 'Open',
    [RECORD_STATUS.CLOSED]: 'Closed'
};
