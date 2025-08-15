import AsyncStorage from '@react-native-async-storage/async-storage';
export async function save(key: string, value: any) { await AsyncStorage.setItem(key, JSON.stringify(value)); }
export async function load(key: string) { const v = await AsyncStorage.getItem(key); return v ? JSON.parse(v) : null; }
export async function clearAll() { await AsyncStorage.clear(); }
