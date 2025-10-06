import React from 'react';
import styles from './ProjectStructureGuide.module.css';

// Define the shape of a single item in our project structure tree
interface StructureItem {
  name: string;
  type: 'folder' | 'file';
  description: string;
  children?: StructureItem[];
}

// Data representing a typical Create React App project structure
const structureData: StructureItem[] = [
    {
        name: 'public/',
        type: 'folder',
        description: 'Static assets not processed by the build tool.',
        children: [
            { name: 'index.html', type: 'file', description: 'The main HTML template for the app.' },
            { name: 'favicon.ico', type: 'file', description: 'The application icon.' },
        ],
    },
    {
        name: 'src/',
        type: 'folder',
        description: 'Your application\'s source code.',
        children: [
            { name: 'components/', type: 'folder', description: 'Reusable UI components.' },
            { name: 'App.tsx', type: 'file', description: 'The root application component.' },
            { name: 'index.tsx', type: 'file', description: 'The entry point that renders the App.' },
            { name: 'App.module.css', type: 'file', description: 'Example of a CSS Module for styling.' },
        ],
    },
    { name: '.gitignore', type: 'file', description: 'Specifies files for Git to ignore.' },
    { name: 'package.json', type: 'file', description: 'Lists project dependencies and scripts.' },
    { name: 'tsconfig.json', type: 'file', description: 'TypeScript compiler configuration.' },
];

// A recursive component to render each node in the structure tree
const StructureNode: React.FC<{ item: StructureItem }> = ({ item }) => (
    <li className={styles.item}>
        <div>
            <span className={item.type === 'folder' ? styles.folder : styles.file}>
                {item.type === 'folder' ? '📁' : '📄'} {item.name}
            </span>
            <span className={styles.description}>- {item.description}</span>
        </div>
        {item.children && (
            <ul className={styles.tree}>
                {item.children.map(child => <StructureNode key={child.name} item={child} />)}
            </ul>
        )}
    </li>
);

// Define the main component's props interface
interface Props {
  projectName: string;
}

/**
 * A component that displays a guide to a typical React project structure,
 * like the one created by Create React App.
 */
const ProjectStructureGuide: React.FC<Props> = ({ projectName }) => {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Project Structure Guide</h1>
      <p>A typical frontend project (e.g., "{projectName}") is structured as follows:</p>
      <ul className={styles.tree}>
        {structureData.map(item => <StructureNode key={item.name} item={item} />)}
      </ul>
    </div>
  );
};

export default ProjectStructureGuide;
