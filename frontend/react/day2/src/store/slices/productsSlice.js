import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

const FAKE_PRODUCTS = [
  { id: 1, title: 'Wireless Headphones', price: 2999 },
  { id: 2, title: 'Mechanical Keyboard', price: 4499 },
  { id: 3, title: 'USB-C Hub', price: 1299 },
  { id: 4, title: 'Webcam HD', price: 3499 },
  { id: 5, title: 'Monitor Stand', price: 1799 },
];

export const fetchProducts = createAsyncThunk('products/fetch', async () => {
  await new Promise(r => setTimeout(r, 600));
  return FAKE_PRODUCTS;
});

const productsSlice = createSlice({
  name: 'products',
  initialState: { items: [], loading: false },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => { state.loading = true; })
      .addCase(fetchProducts.fulfilled, (state, action) => { state.loading = false; state.items = action.payload; });
  },
});

export default productsSlice.reducer;
