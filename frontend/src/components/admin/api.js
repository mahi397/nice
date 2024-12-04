// src/services/api.js
const API_URL = "http://localhost:8000/nice/admin"; // Django backend API URL

export const getTrips = async () => {
//   const response = await fetch(`${API_URL}/trips/`);
//   return await response.json();
    return [
        { id: 1, name: 'Bahamas Cruise', startPort: 'Miami', endPort: 'Bahamas', startMonth: 'December', duration: 4, imageUrl: 'https://via.placeholder.com/150' },
        { id: 2, name: 'Caribbean Cruise', startPort: 'Miami', endPort: 'Jamaica', startMonth: 'January', duration: 7, imageUrl: 'https://via.placeholder.com/150' },
        { id: 3, name: 'Alaska Cruise', startPort: 'Seattle', endPort: 'Alaska', startMonth: 'June', duration: 10, imageUrl: 'https://via.placeholder.com/150' },
      ];
};

export const getShips = async () => {
    const response = await fetch(`${API_URL}/ships/`);
    return await response.json();
};

export const getPorts = async () => {
  const response = await fetch(`${API_URL}/ports/`);
  return await response.json();
};

export const getUsers = async () => {
  const response = await fetch(`${API_URL}/users/`);
  return await response.json();
};

export const getActivities = async () => {
    const response = await fetch(`${API_URL}/activities/`);
    return await response.json();
  };

export const getRestaurants = async () => {
    const response = await fetch(`${API_URL}/restaurants/`);
    return await response.json();
  };

export const updateRecord = async (entity, id, data) => {
  const response = await fetch(`${API_URL}/${entity}/${id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return await response.json();
};

export const deleteRecord = async (entity, id) => {
  await fetch(`${API_URL}/${entity}/${id}/`, {
    method: "DELETE",
  });
};

export const addRecord = async (entity, data) => {
  const response = await fetch(`${API_URL}/${entity}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return await response.json();
};
