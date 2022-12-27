import Head from "next/head";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/router";
import styles from "../styles/Home.module.css";

export default function Home() {
  const router = useRouter();
  return (
    <div className={styles.container}>
      <Head>
        <title>Fastapi Sample Frontend</title>
      </Head>

      <h1 className={styles.title}>Fastapi Sample Frontend</h1>

      <div className={styles.main}>
        <div className={styles.link}>
          <div>
            <a href="http://localhost:8888/docs">BackendAPI(Swagger)</a>
          </div>
          <div>
            <a href="/todos/list">Todos List</a>
          </div>
          <div>
            <a href="/todos/create">Todos Create</a>
          </div>
        </div>
      </div>
    </div>
  );
}
