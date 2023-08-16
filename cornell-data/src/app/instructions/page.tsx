import { ReactNode } from 'react';

function CodeBlock({ children }: { children: ReactNode }) {
    return (
        <pre className="bg-gray-400 rounded p-2 ml-4 overflow-auto w-fit">
            <code>{children}</code>
        </pre>
    );
}

export default function Instructions() {
    return (
        <div className="p-6">
            <h1 className="text-4xl font-bold mb-4">Instructions</h1>

            <div className="my-4">
                <div className="p-4 bg-gray-100 rounded mt-2">
                    <h2 className="text-2xl font-bold mb-2">Setup</h2>
                    <ol className="list-none list-inside ml-5 space-y-3 list">
                        <li>Open a Terminal (MacOS) or Command Prompt (Windows) window and navigate to the directory where you want to store the project.</li>
                        <li>
                            Clone the repository: Run <CodeBlock>git clone repository-url</CodeBlock> to clone the repository to your local system.
                        </li>
                        <li>
                            Navigate to the repository: Use <CodeBlock>cd repository-directory</CodeBlock> to go to the cloned repository&apos;s directory.
                        </li>
                        <li>
                            Create a Python virtual environment to isolate the project&apos;s dependencies: On Unix or MacOS, run:{' '}
                            <CodeBlock>python3 -m venv env</CodeBlock>. On Windows, run:
                            <CodeBlock>py -m venv env</CodeBlock>
                        </li>
                        <li>
                            Activate the virtual environment: On Unix or MacOS, run: <CodeBlock>source env/bin/activate</CodeBlock>. On Windows, run:
                            <CodeBlock>.\env\Scripts\activate</CodeBlock>.
                        </li>
                        <li>
                            Install the required dependencies: Use <CodeBlock>pip install -r requirements.txt</CodeBlock> to install all necessary dependencies.
                        </li>
                        <li>
                            Prepare the data: Create a <u>data</u> folder at the root of the project and add the Excel sheets provided by the project manager.
                        </li>
                        <li>
                            Set environment variables: Create a <u>.env</u> file at the root of the project with your Cornell NetID and password.
                            <CodeBlock>
                                NETID=your-netid
                                <br />
                                PASSWORD=your-password
                            </CodeBlock>
                        </li>
                    </ol>
                </div>
            </div>

            <div className="my-4">
                <div className="p-4 bg-gray-100 rounded mt-2">
                    <h2 className="text-2xl font-bold mb-2">Usage</h2>
                    <p>
                        Once the setup is complete, you can run the program using the command <CodeBlock>python index.py</CodeBlock>. Optionally, you can add
                        the <CodeBlock>--mergent</CodeBlock> or <CodeBlock>--guidestar</CodeBlock> flags to run specific scraping functionalities. If no flag is
                        provided, the program will run both functionalities concurrently.
                    </p>
                </div>
            </div>
        </div>
    );
}
