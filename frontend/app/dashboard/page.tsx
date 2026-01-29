import ChatWindow from "../components/chat/ChatWindow";

export default function Dashboard() {
    return (
        <main className="min-h-screen bg-slate-100 dark:bg-slate-950 p-8">
            <div className="max-w-6xl mx-auto space-y-8">
                <header className="flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Dashboard</h1>
                        <p className="text-slate-500">Welcome back, Charan</p>
                    </div>
                    <div className="h-10 w-10 bg-gradient-to-tr from-blue-500 to-purple-500 rounded-full" />
                </header>

                <section className="grid md:grid-cols-3 gap-6">
                    {/* Quick Stats Card */}
                    <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
                        <h3 className="text-sm font-medium text-slate-500">Total Properties</h3>
                        <p className="text-2xl font-bold mt-2">12</p>
                    </div>
                    <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
                        <h3 className="text-sm font-medium text-slate-500">Active Issues</h3>
                        <p className="text-2xl font-bold mt-2 text-red-500">3</p>
                    </div>
                    <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
                        <h3 className="text-sm font-medium text-slate-500">Monthly Revenue</h3>
                        <p className="text-2xl font-bold mt-2 text-green-500">$45,200</p>
                    </div>
                </section>

                <section>
                    <h2 className="text-xl font-semibold mb-4 text-slate-700 dark:text-slate-300">AI Assistant</h2>
                    <ChatWindow />
                </section>
            </div>
        </main>
    );
}
