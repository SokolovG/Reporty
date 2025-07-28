export const RECORD_STATUS = {
    OPEN: 'OPEN',
    CLOSED: 'CLOSED'
};

export const STATUS_STYLES = {
    [RECORD_STATUS.OPEN]: 'bg-green-100 text-green-700',
    [RECORD_STATUS.CLOSED]: 'bg-red-100 text-red-700'
};

export const STATUS_LABELS = {
    [RECORD_STATUS.OPEN]: 'Open',
    [RECORD_STATUS.CLOSED]: 'Closed'
};
