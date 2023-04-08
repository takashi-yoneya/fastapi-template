import { TodoCreate, TodoUpdate } from "api_clients";
import {
  useCreateTodo,
  useGetTodoById,
  useUpdateTodo,
} from "lib/hooks/api/todos";
import { useRouter } from "next/router";
import { FC, useCallback, useEffect, useState } from "react";

const TodoCreateTemplate: FC = () => {
  const [requestData, setRequestData] = useState<TodoCreate>({
    title: "",
    description: "",
  });
  const [isSuccess, setIsSuccess] = useState<boolean>(false);
  const router = useRouter();
  const { mutateAsync: createMutateAsync, isLoading: isLoading } =
    useCreateTodo();

  const handleChangeValue = useCallback(
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
      const { name, value } = e.target;
      setRequestData({
        ...requestData,
        [name]: value,
      });
    },
    [setRequestData, requestData],
  );

  const handleClickUpdateButton = async (): Promise<void> => {
    if (!requestData) return;
    await createMutateAsync(
      requestData,
      (responseData) => {
        setIsSuccess(true);
        console.log("success.", responseData);
      },
      (error) => {
        setIsSuccess(false);
        console.log("error.", error);
      },
    );
  };
  return (
    <div>
      <h2>Todo Create</h2>
      <div>
        タイトル:
        <input
          name="title"
          value={requestData?.title}
          onChange={handleChangeValue}
        />
      </div>
      <div>
        説明:
        <textarea
          name="description"
          value={requestData?.description}
          onChange={handleChangeValue}
        />
      </div>
      <button onClick={() => router.back()}>キャンセル</button>
      <button onClick={handleClickUpdateButton}>登録</button>
      <div>{isLoading && "処理中"}</div>
      <div>{!isLoading && isSuccess && "完了"}</div>
    </div>
  );
};

export default TodoCreateTemplate;
