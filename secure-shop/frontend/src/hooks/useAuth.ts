// hooks/useAuth.ts
import { useAuthContext } from '../context/AuthContext';
import { login as loginService, register as registerService } from '../services/authService';

export const useAuth = () => {
  const { login: setToken, logout: setLogout, isAuthenticated } = useAuthContext();

  const login = async (email: string, password: string) => {
    const response = await loginService({ email, password });
    setToken(response.access_token);
    return response;
  };

  const register = async (username: string, email: string, password: string) => {
    await registerService({ username, email, password });
  };

  const logout = () => {
    localStorage.removeItem('token');
    setLogout();
  };

  return { login, register, logout, isAuthenticated };
};