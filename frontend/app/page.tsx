import Link from "next/link";
import { ArrowRight, Building, ShieldCheck, Zap } from "lucide-react";

export default function Home() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-between p-24 bg-slate-950 text-white selection:bg-blue-500 selection:text-white">
            <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
                <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
                    AI Property Management System
                </p>
                <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">
                    <div className="pointer-events-none flex place-items-center gap-2 p-8 lg:pointer-events-auto lg:p-0">
                        <span>v1.0.0</span>
                    </div>
                </div>
            </div>

            <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-to-tr before:from-blue-400 before:to-purple-500 before:blur-2xl before:content-[''] before:z-[-1] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-to-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px]">
                <div className="text-center">
                    <h1 className="text-6xl font-bold tracking-tighter sm:text-7xl bg-clip-text text-transparent bg-gradient-to-r from-blue-200 via-blue-400 to-purple-600 mb-6">
                        Autonomy for <br /> Your Assets
                    </h1>
                    <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10">
                        The first truly agentic property management platform. Let AI handle tenants, maintenance, and finance while you sleep.
                    </p>

                    <div className="flex gap-4 justify-center">
                        <Link href="/dashboard" className="group rounded-full border border-transparent px-5 py-3 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30 bg-blue-600 hover:!bg-blue-700 text-white font-semibold flex items-center gap-2">
                            Get Started <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </Link>
                        <Link href="/demo" className="rounded-full border border-slate-700 px-5 py-3 hover:bg-slate-800 transition-colors">
                            Watch Demo
                        </Link>
                    </div>
                </div>
            </div>

            <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-3 lg:text-left gap-8">
                <FeatureCard
                    title="Smart Agents"
                    desc="Dedicated agents for leasing, support, and maintenance coordination."
                    icon={<Zap className="w-6 h-6 text-yellow-400" />}
                />
                <FeatureCard
                    title="Automated Legal"
                    desc="Region-aware compliance checks and auto-generated lease agreements."
                    icon={<ShieldCheck className="w-6 h-6 text-green-400" />}
                />
                <FeatureCard
                    title="Portfolio Analytics"
                    desc="Real-time financial insights and vacancy risk prediction."
                    icon={<Building className="w-6 h-6 text-blue-400" />}
                />
            </div>
        </main>
    );
}

function FeatureCard({ title, desc, icon }: { title: string, desc: string, icon: React.ReactNode }) {
    return (
        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
            <h2 className={`mb-3 text-2xl font-semibold flex items-center gap-3`}>
                {icon}
                {title}
                <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                    -&gt;
                </span>
            </h2>
            <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
                {desc}
            </p>
        </div>
    )
}
