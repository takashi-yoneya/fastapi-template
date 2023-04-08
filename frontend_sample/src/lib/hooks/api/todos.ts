import type { UseGetResult, UsePostResult } from ".";
import { useGet, usePost } from ".";
import { ErrorResponse } from "types/api";
import internal from "stream";
import {
  TodoCreate,
  TodoResponse,
  TodosPagedResponse,
  TodoUpdate,
} from "api_clients";
import { TodosApiClient } from "api_clients/client";

export const useGetTodoById = (id?: string): UseGetResult<TodoResponse> =>
  useGet([`/todos`, id], async () =>
    id ? TodosApiClient.getTodoById(id) : Promise.reject(),
  );

type GetJobsProps = {
  q?: string;
  page?: number;
  perPage?: number;
};

export const useGetTodos = (
  props: GetJobsProps,
): UseGetResult<TodosPagedResponse> => {
  const { q, page, perPage } = props;
  return useGet([`/todos`, q, page, perPage], async () =>
    TodosApiClient.getTodos(q, page, perPage),
  );
};

export const useCreateTodo = (): UsePostResult<
  TodoResponse,
  ErrorResponse,
  TodoCreate
> =>
  usePost([`/todos`], async (request: TodoCreate) =>
    TodosApiClient.createTodo(request),
  );

export const useUpdateTodo = (
  id?: string,
): UsePostResult<TodoResponse, ErrorResponse, TodoUpdate> => {
  return usePost([`/todos`, id], async (request: TodoUpdate) =>
    id ? TodosApiClient.updateTodo(id, request) : Promise.reject(),
  );
};
