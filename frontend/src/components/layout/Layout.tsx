export function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-zinc-50 flex flex-col">
            <header className="bg-white border-b border-zinc-200">
                <div className="max-w-7xl mx-auto px-4 h-16 flex items-center">
                    <h1 className="text-1xl font-bold text-zinc-900 tracking-tight">
                        Métricas do ENEM
                    </h1>
                </div>
            </header>

            <main className="flex-1 max-w-7xl mx-auto px-4 py-8 w-full">
                {children}
            </main>
        </div>
    )
}