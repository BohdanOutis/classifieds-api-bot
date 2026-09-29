interface SpinnerProps {
  size?: number;
  className?: string;
}

const Spinner = ({ size = 32, className = '' }: SpinnerProps) => (
  <svg
    className={`spinner ${className}`}
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-label="Loading..."
    role="status"
  >
    <circle
      className="spinner__track"
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      strokeWidth="2"
      strokeOpacity="0.2"
    />
    <path
      className="spinner__arc"
      d="M12 2a10 10 0 0 1 10 10"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
);

export default Spinner;