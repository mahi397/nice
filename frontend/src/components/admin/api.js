import axios from "axios";
import { API_URL } from "../../constants";

// Function to refresh the access token
// export const refreshAccessToken = async () => {
//   const refreshToken = localStorage.getItem("refreshToken");
//   try {
//     const response = await axios.post(`${API_URL}/token/refresh`, {
//       refresh: refreshToken,
//     });

//     if (response.data.access) {
//       localStorage.setItem("authToken", response.data.access);
//       console.log("New access token set in localStorage:", response.data.access);
//       return response.data.access;
//     } else {
//       console.error("Failed to refresh access token");
//       throw new Error("Failed to refresh access token");
//     }
//   } catch (error) {
//     console.error("Error refreshing access token:", error);
//     throw error;
//   }
// };

export const getEntity = async (entity) => {
  let token = localStorage.getItem("authToken");
  try {
    const response = await axios.get(`${API_URL}/admin/${entity}/list`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return await response.data;
  } catch (error) {
    // Handle any errors (optional, logging here)
    console.error(`Error fetching ${entity} data:`, error);
    throw error; // Re-throw the error so the caller knows something went wrong
  }
};

export const getTrips = async () => {
  //   const response = await fetch(`${API_URL}/ports/list`);
  //   return await response.json();
  return [
    {
      id: 1,
      name: "Bahamas Cruise",
      startPort: "Miami",
      endPort: "Bahamas",
      startMonth: "December",
      duration: 4,
      imageUrl: "https://via.placeholder.com/150",
    },
    {
      id: 2,
      name: "Caribbean Cruise",
      startPort: "Miami",
      endPort: "Jamaica",
      startMonth: "January",
      duration: 7,
      imageUrl: "https://via.placeholder.com/150",
    },
    {
      id: 3,
      name: "Alaska Cruise",
      startPort: "Seattle",
      endPort: "Alaska",
      startMonth: "June",
      duration: 10,
      imageUrl: "https://via.placeholder.com/150",
    },
  ];
};

// Example API call that uses the access token
export const getShips = async () => {
  let token = localStorage.getItem("authToken");
  try {
    const response = await fetch(`${API_URL}/admin/ships/list`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // if (response.status === 401) {
    //   // Token might be expired, try to refresh it
    //   token = await refreshAccessToken();
    //   // Retry the request with the new token
    //   const retryResponse = await fetch(`${API_URL}/ships/list`, {
    //     headers: {
    //       'Authorization': `Bearer ${token}`
    //     }
    //   });
    //   return await retryResponse.json();
    // }

    return await response.json();
  } catch (error) {
    console.error("Error fetching ships data:", error);
    throw error;
  }
};

export const getPorts = async () => {
  let token = localStorage.getItem("authToken");
  try {
    const response = await fetch(`${API_URL}/admin/ports/list`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // if (response.status === 401) {
    //   // Token might be expired, try to refresh it
    //   token = await refreshAccessToken();
    //   // Retry the request with the new token
    //   const retryResponse = await fetch(`${API_URL}/ports/`, {
    //     headers: {
    //       'Authorization': `Bearer ${token}`
    //     }
    //   });
    //   return await retryResponse.json();
    // }

    return await response.json();
  } catch (error) {
    console.error("Error fetching ports data:", error);
    throw error;
  }
};

export const getUsers = async () => {
  const response = await fetch(`${API_URL}/admin/users/list`);
  return await response.json();
};

export const getActivities = async () => {
  const response = await fetch(`${API_URL}/admin/activities/list`);
  return await response.json();
};

export const getRestaurants = async () => {
  const response = await fetch(`${API_URL}/admin/restaurants/list`);
  return await response.json();
};

export const getPackages = async () => {
  const response = await fetch(`${API_URL}/admin/packages/list`);
  return await response.json();
};

export const addRecord = async (entity, data) => {
  const response = await fetch(`${API_URL}/admin/${entity}/add`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return await response.json();
};

export const updateRecord = async (entity, id, data) => {
  const response = await fetch(`${API_URL}/admin/${entity}/${id}/update`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return await response.json();
};

export const deleteRecord = async (entity, id) => {
  await fetch(`${API_URL}/admin/${entity}/${id}/delete`, {
    method: "DELETE",
  });
};
