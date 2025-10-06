import React, { useState, useEffect, FC, FormEvent, ChangeEvent } from 'react';
import styles from './TaskManager.module.css';

// --- Type Definitions ---
interface Task {
  id: number;
  title: string;
  completed: boolean;
}

// In a real app, these API functions and the mock data would be in a separate service file.
// --- Mock API Service ---

const API_LATENCY = 500; // Simulate network delay in ms

// Mock database
let mockTasks: Task[] = [
  { id: 1, title: 'Learn React Hooks', completed: true },
  { id: 2, title: 'Write TypeScript code', completed: true },
  { id: 3, title: 'Use CSS Modules', completed: false },
];
let nextId = 4;

/**
 * Fetches the list of all tasks.
 */
const fetchTasks = async (): Promise<Task[]> => {
  console.log('Fetching tasks...');
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log('Fetched tasks:', mockTasks);
      resolve([...mockTasks]); // Return a copy to prevent mutation
    }, API_LATENCY);
  });
};

/**
 * Creates a new task.
 * @param title - The title of the new task.
 */
const createTask = async (title: string): Promise<Task> => {
  console.log(`Creating task with title: "${title}"`);
  return new Promise((resolve) => {
    setTimeout(() => {
      const newTask: Task = {
        id: nextId++,
        title,
        completed: false,
      };
      mockTasks.push(newTask);
      console.log('Created task:', newTask);
      resolve(newTask);
    }, API_LATENCY);
  });
};

/**
 * Updates an existing task.
 * @param id - The ID of the task to update.
 * @param updates - An object with the task properties to update.
 */
const updateTask = async (id: number, updates: Partial<Omit<Task, 'id'>>): Promise<Task> => {
  console.log(`Updating task ${id} with:`, updates);
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const taskIndex = mockTasks.findIndex((task) => task.id === id);
      if (taskIndex === -1) {
        return reject(new Error('Task not found'));
      }
      mockTasks[taskIndex] = { ...mockTasks[taskIndex], ...updates };
      console.log('Updated task:', mockTasks[taskIndex]);
      resolve(mockTasks[taskIndex]);
    }, API_LATENCY);
  });
};

// --- Component Props ---
// This component is self-contained and fetches its own data, so it doesn't require props.
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface Props {}

/**
 * TaskManager component that demonstrates fetching, creating, and updating tasks.
 */
const TaskManager: FC<Props> = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [newTaskTitle, setNewTaskTitle] = useState<string>('');

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedTasks = await fetchTasks();
      setTasks(fetchedTasks);
    } catch (err) {
      setError('Failed to fetch tasks.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleCreateTask = async (e: FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
        setLoading(true);
        const createdTask = await createTask(newTaskTitle);
        setTasks(prevTasks => [...prevTasks, createdTask]);
        setNewTaskTitle('');
    } catch (err) {
        setError('Failed to create task.');
        console.error(err);
    } finally {
        setLoading(false);
    }
  };
  
  const handleToggleComplete = async (taskToUpdate: Task) => {
    try {
        const updatedTask = await updateTask(taskToUpdate.id, { completed: !taskToUpdate.completed });
        setTasks(prevTasks => prevTasks.map(task => 
            task.id === updatedTask.id ? updatedTask : task
        ));
    } catch (err) {
        setError('Failed to update task.');
        console.error(err);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.header}>Task Manager</h1>
      
      <form onSubmit={handleCreateTask} className={styles.form}>
        <input
          type="text"
          value={newTaskTitle}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setNewTaskTitle(e.target.value)}
          placeholder="Enter a new task title"
          className={styles.input}
          disabled={loading}
        />
        <button type="submit" className={styles.button} disabled={loading || !newTaskTitle.trim()}>
          Add Task
        </button>
      </form>
      
      <div className={styles.controls}>
        <button onClick={loadTasks} disabled={loading} className={styles.button}>
          {loading ? 'Loading...' : 'Refresh Tasks'}
        </button>
      </div>

      {error && <p className={styles.error}>{error}</p>}
      
      {loading && tasks.length === 0 ? (
        <p className={styles.loadingText}>Loading tasks...</p>
      ) : (
        <ul className={styles.taskList}>
          {tasks.map((task) => (
            <li key={task.id} className={`${styles.taskItem} ${task.completed ? styles.completed : ''}`}>
              <span onClick={() => handleToggleComplete(task)} className={styles.taskTitle}>
                {task.title}
              </span>
              <button onClick={() => handleToggleComplete(task)} className={styles.toggleButton}>
                {task.completed ? 'Undo' : 'Complete'}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskManager;
