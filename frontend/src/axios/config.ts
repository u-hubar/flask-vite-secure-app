import Axios from 'axios';

const headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Cache-Control': 'no-cache',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Access-Control-Allow-Origin': '*',
};

export const api = Axios.create({
  baseURL: `https://${window.location.hostname}/core/`,
  responseType: 'json',
  headers,
});
