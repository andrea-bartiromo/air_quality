export const useApi = () => {
  const config = useRuntimeConfig()
  const base = config.public.apiBase
  const get = async <T>(path: string) => {
    const { data, error } = await useFetch<T>(`${base}${path}`, { key: path })
    if (error.value) throw createError(error.value)
    return data.value as T
  }
  return { get }
}
