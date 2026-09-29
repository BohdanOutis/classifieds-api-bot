type Status = 'active' | 'pending' | 'inactive' | 'rejected' | string;

interface StatusBadgeProps {
  status: Status;
}

const statusConfig: Record<string, { label: string; className: string }> = {
  active: { label: 'Активне', className: 'badge badge--active' },
  pending: { label: 'На модерації', className: 'badge badge--pending' },
  inactive: { label: 'Неактивне', className: 'badge badge--inactive' },
  rejected: { label: 'Відхилено', className: 'badge badge--rejected' },
};

const StatusBadge = ({ status }: StatusBadgeProps) => {
  const config = statusConfig[status] ?? {
    label: status,
    className: 'badge badge--default',
  };
  return <span className={config.className}>{config.label}</span>;
};

export default StatusBadge;