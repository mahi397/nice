import { API_URL } from "../../constants";

export const getStartBookingURL = (tripId) => `${API_URL}/trips/list/${tripId}/start-booking/`;

export const getTripCapacityReserveURL = (tripId) => `${API_URL}/trips/${tripId}/reserve-temporary-capacity/`;

export const getRoomReserveURL = (tripId) => `${API_URL}/trips/${tripId}/reserve-temporary-rooms/`;

export const getPkgListURL = (tripId) => `${API_URL}/trips/${tripId}/package-details/`;

export const getAddPkgURL = (tripId) => `${API_URL}/trips/${tripId}/add-package/`;

export const getAddPassengerURL = (tripId) => `${API_URL}/trips/${tripId}/add-passenger-details/`;
