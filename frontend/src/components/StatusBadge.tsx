type Status = 'active' | 'pending' | 'inactive' | 'rejected' | string;

interface StatusBadgeProps {
  status: Status;
}

const baseClasses =
  'inline-flex items-center px-2.5 py-0.5 rounded-full text-[0.7rem] font-bold tracking-wider uppercase whitespace-nowrap';

const statusConfig: Record<string, { label: string; className: string }> = {
  active: {
    label: 'Активне',
    className: 'bg-green-500/15 text-green-400 border border-green-500/30',
  },
  pending: {
    label: 'На модерації',
    className: 'bg-amber-500/15 text-amber-400 border border-amber-500/30',
  },
  inactive: {
    label: 'Неактивне',
    className: 'bg-slate-500/15 text-slate-400 border border-slate-500/30',
  },
  rejected: {
    label: 'Відхилено',
    className: 'bg-red-500/15 text-red-400 border border-red-500/30',
  },
};

const defaultStyle = {
  bg: 'bg-[var(--clr-surface-3)]',
  text: 'text-[var(--clr-text-2)]',
  border: 'border border-[var(--clr-border)]',
};

const StatusBadge = ({ status }: StatusBadgeProps) => {
  const config = statusConfig[status];

  const label = config?.label ?? status;
  const variantClasses = config?.className ?? `${defaultStyle.bg} ${defaultStyle.text} ${defaultStyle.border}`;

  return <span className={`${baseClasses} ${variantClasses}`}>{label}</span>;
};

export default StatusBadge;