import { Navigate } from "react-router-dom";
import { getSession } from "../../api/auth";

export default function ProtectedRoute({ children, roles }) {
  const session = getSession();
  if (!session) return <Navigate to="/login" replace />;
  if (!roles.includes(session.role)) return <Navigate to="/" replace />;
  return children;
}
