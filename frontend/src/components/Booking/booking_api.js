import { API_URL } from "../../constants";
export const getStartBookingURL = (tripId) => `${API_URL}/trips/list/${tripId}/start-booking/`;
