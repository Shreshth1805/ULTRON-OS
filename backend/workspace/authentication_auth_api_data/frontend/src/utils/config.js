export const API_URL = 'http://localhost:8080/api';
export const TASKS_ENDPOINT = '/tasks';
export const USERS_ENDPOINT = '/users';
export const LOGIN_ENDPOINT = '/login';
export const REGISTER_ENDPOINT = '/register';

export const getConfig = () => {
  return {
    headers: {
      'Content-Type': 'application/json',
    },
  };
};

export const getAuthConfig = (token) => {
  return {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  };
};

export const handleResponse = (response) => {
  if (response.ok) {
    return response.json();
  } else {
    throw new Error(response.statusText);
  }
};

export const handleError = (error) => {
  console.error(error);
  throw error;
};