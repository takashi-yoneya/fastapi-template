import type { AxiosError, AxiosResponse } from "axios";
import type {
  QueryFunction,
  UseQueryOptions,
  UseQueryResult,
  MutateFunction,
  UseMutationOptions,
  UseMutationResult,
} from "react-query";
import { useQuery, useMutation } from "react-query";

export type UseGetResult<TData, TError = ErrorResponse> = Omit<
  UseQueryResult<AxiosResponse<TData>, AxiosError<TError>>,
  "data" | "error"
> & {
  data?: TData;
  error?: TError;
};

export type UsePostResult<
  TData,
  TError = ErrorResponse,
  TVariables = unknown,
> = Omit<
  UseMutationResult<AxiosResponse<TData>, AxiosError<TError>, TVariables>,
  "mutateAsync"
> & {
  mutateAsync: (
    variables: TVariables,
    onSuccess?: (data: TData) => unknown,
    onFailure?: (error?: TError) => unknown,
  ) => Promise<unknown>;
};

export type ErrorResponse = {
  errorCode?: string;
  errorMessage?: string;
};

export const useGet = <TData, TError = ErrorResponse>(
  key: unknown[] | string,
  queryFn: QueryFunction<AxiosResponse<TData>>,
  options?: UseQueryOptions<AxiosResponse<TData>, AxiosError<TError>>,
): UseGetResult<TData, TError> => {
  const result = useQuery<
    AxiosResponse<TData>,
    AxiosError<TError>,
    AxiosResponse<TData>
  >(key, queryFn, options);
  return {
    ...result,
    data: result.data?.data,
    error: result.error?.response?.data,
  };
};

export const usePost = <TData, TError = ErrorResponse, TVariables = unknown>(
  key: unknown[] | string,
  mutationFn: MutateFunction<
    AxiosResponse<TData>,
    AxiosError<TError>,
    TVariables
  >,
  options?: Omit<
    UseMutationOptions<AxiosResponse<TData>, AxiosError<TError>, TVariables>,
    "mutationFn" | "mutationKey"
  >,
): UsePostResult<TData, TError, TVariables> => {
  const result = useMutation<
    AxiosResponse<TData>,
    AxiosError<TError>,
    TVariables
  >(key, mutationFn, options);
  return {
    ...result,
    mutateAsync: async (
      variables: TVariables,
      onSuccess?: (data: TData) => unknown,
      onFailure?: (error?: TError) => unknown,
    ) =>
      result
        .mutateAsync(variables)
        .then((res) => onSuccess?.(res.data))
        .catch((error: AxiosError<TError>) => {
          onFailure ? onFailure?.(error?.response?.data) : console.log(error);
        }),
  };
};
